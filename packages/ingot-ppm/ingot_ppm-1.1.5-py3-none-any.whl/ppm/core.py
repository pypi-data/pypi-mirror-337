import os
import sys
import json
import asyncio
import aiohttp
import zipfile
import tarfile
import tempfile
import shutil
from pathlib import Path
from packaging import version
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn

def safe_extractall(tar, path=".", members=None):
    """安全地解压tar文件，防止路径遍历漏洞"""
    def is_within_directory(directory, target):
        abs_directory = os.path.abspath(directory)
        abs_target = os.path.abspath(target)
        prefix = os.path.commonprefix([abs_directory, abs_target])
        return prefix == abs_directory

    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise Exception("路径遍历攻击检测：检测到恶意文件路径")
    
    tar.extractall(path, members)

class Package:
    def __init__(self, name, version):
        self.name = name
        self.version = version

class PackageManager:
    PYPI_MIRROR = "https://pypi.tuna.tsinghua.edu.cn/simple"
    PYPI_JSON = "https://pypi.tuna.tsinghua.edu.cn/pypi"
    
    def __init__(self):
        self.site_packages = Path(sys.prefix) / "Lib" / "site-packages"
        self.package_list = {}
        self.session = None
    
    async def _init_session(self):
        if not self.session or self.session.closed:
            self.session = aiohttp.ClientSession()
            
    async def _close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def _get_package_info(self, package_name):
        try:
            await self._init_session()
            async with self.session.get(f"{self.PYPI_JSON}/{package_name}/json") as response:
                if response.status == 200:
                    content_type = response.headers.get('Content-Type', '')
                    if 'application/json' not in content_type and 'application/octet-stream' not in content_type:
                        print(f"警告：意外的Content-Type: {content_type}")
                    return await response.json(content_type=None)
                return None
        except aiohttp.ClientError as e:
            print(f"获取包信息时发生错误: {e}")
            return None

    
    async def _download_package(self, url, filename, progress):
        await self._init_session()
        task_id = progress.add_task(f"Downloading {filename}...", total=None)
        async with self.session.get(url) as response:
            total = int(response.headers.get('content-length', 0))
            progress.update(task_id, total=total)
            
            with open(filename, 'wb') as f:
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    progress.update(task_id, advance=len(chunk))
    
    def install_package(self, package_name, latest=False, version=None):
        async def _install():
            try:
                info = await self._get_package_info(package_name)
                if not info:
                    print(f"Package {package_name} not found")
                    return
                
                if not info.get('releases'):
                    print(f"No releases found for {package_name}")
                    return
                
                if version:
                    if version not in info['releases']:
                        print(f"Version {version} not found for {package_name}")
                        return
                    target_version = version
                else:
                    try:
                        if not info['releases']:
                            print(f"未找到{package_name}的任何版本")
                            return
                        versions = [v for v in info['releases'].keys() if v and isinstance(v, str)]
                        if not versions:
                            print(f"未找到{package_name}的有效版本信息")
                            return
                        versions = sorted(versions, key=lambda v: version.parse(v))
                        if not versions:
                            print(f"无法解析{package_name}的版本信息")
                            return
                        target_version = versions[-1] if latest else versions[0]
                    except KeyError:
                        print(f"获取{package_name}的版本信息失败：数据格式错误")
                        return
                    except Exception as e:
                        print(f"解析{package_name}版本时发生错误: {e}")
                        return
            
                try:
                    release = info['releases'][target_version][0]
                    filename = release['filename']
                    url = release['url']
                    if url.startswith("https://pypi.org"):
                        url = url.replace("https://pypi.org", self.PYPI_MIRROR)
                    elif url.startswith("https://files.pythonhosted.org"):
                        url = url.replace("https://files.pythonhosted.org", self.PYPI_MIRROR)
                    
                    with Progress(
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        DownloadColumn(),
                        TransferSpeedColumn(),
                    ) as progress:
                        await self._download_package(url, filename, progress)
                    
                    # 解压并安装包
                    install_dir = Path(tempfile.mkdtemp())
                    try:
                        if filename.endswith('.whl'):
                            with zipfile.ZipFile(filename) as wheel:
                                wheel.extractall(install_dir)
                        elif filename.endswith('.tar.gz'):
                            with tarfile.open(filename, 'r:gz') as tar:
                                safe_extractall(tar, install_dir)
                        elif filename.endswith('.zip'):
                            with zipfile.ZipFile(filename) as zip_file:
                                zip_file.extractall(install_dir)
                        
                        # 安装包文件
                        for item in install_dir.rglob('*.py'):
                            try:
                                if item.parent.name == 'site-packages':
                                    continue
                                # 尝试找到最近的包目录或安装目录作为基准点
                                base_dir = next((p for p in item.parents
                                    if p.name.endswith(('-dist-info', '.egg-info'))
                                    or any(f.name.endswith(('.dist-info', '.egg-info')) for f in p.iterdir())
                                    or p == install_dir),
                                    install_dir)
                                relative_path = item.relative_to(base_dir)
                                dest = self.site_packages / relative_path
                                if not dest.parent.exists():
                                    dest.parent.mkdir(parents=True, exist_ok=True)
                                shutil.copy2(item, dest)
                            except (ValueError, StopIteration) as e:
                                print(f"跳过文件：{item} - 无法确定相对路径: {e}")
                                continue
                            except Exception as e:
                                print(f"复制文件时发生错误: {e}")
                                continue
                        
                        # 复制dist-info
                        dist_info = next(install_dir.rglob('*.dist-info'), None)
                        if dist_info:
                            dest_info = self.site_packages / dist_info.name
                            if dest_info.exists():
                                shutil.rmtree(dest_info)
                            shutil.copytree(dist_info, dest_info)
                        
                        print(f"Successfully installed {package_name} {target_version}")
                    except Exception as e:
                        print(f"解压或安装文件时发生错误: {e}")
                        if os.path.exists(filename):
                            os.remove(filename)
                        if os.path.exists(install_dir):
                            shutil.rmtree(install_dir)
                        return
                except Exception as e:
                    print(f"安装过程中发生错误: {e}")
            finally:
                # 清理临时文件
                try:
                    if 'install_dir' in locals():
                        shutil.rmtree(install_dir)
                    if 'filename' in locals() and os.path.exists(filename):
                        os.remove(filename)
                except Exception as e:
                    print(f"清理临时文件时发生错误: {e}")
                # 确保会话被正确关闭
                await self._close_session()
        
        try:
            asyncio.run(_install())
        except Exception as e:
            print(f"执行安装任务时发生错误: {e}")
            if self.session and not self.session.closed:
                asyncio.run(self.session.close())
    
    def list_packages(self):
        packages = []
        for path in self.site_packages.glob("*.dist-info"):
            name = path.name.split("-")[0]
            ver = path.name.split("-")[1]
            packages.append(Package(name, ver))
        return packages
    
    async def _check_package_updates(self):
        updates_available = []
        for pkg in self.list_packages():
            info = await self._get_package_info(pkg.name)
            if info:
                latest_version = sorted(info['releases'].keys(), key=version.parse)[-1]
                if version.parse(latest_version) > version.parse(pkg.version):
                    updates_available.append((pkg.name, pkg.version, latest_version))
        return updates_available

    def update_package_list(self):
        async def _update():
            updates = await self._check_package_updates()
            if not updates:
                print("所有包都是最新版本")
                return
            
            print("发现以下包有更新：")
            for name, current_ver, latest_ver in updates:
                print(f"{name}: {current_ver} -> {latest_ver}")
            
            for name, _, _ in updates:
                self.install_package(name, latest=True)
        
        asyncio.run(_update())
    
    def update_self(self):
        async def _update():
            info = await self._get_package_info("ppm")
            if not info:
                print("无法获取PPM版本信息")
                return
            
            latest_version = sorted(info['releases'].keys(), key=version.parse)[-1]
            current_version = __version__
            
            if version.parse(latest_version) > version.parse(current_version):
                print(f"发现新版本：{latest_version}")
                self.install_package("ppm", latest=True)
            else:
                print("PPM已是最新版本")
        
        asyncio.run(_update())
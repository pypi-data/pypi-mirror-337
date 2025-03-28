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
        if not self.session:
            self.session = aiohttp.ClientSession()
    
    async def _get_package_info(self, package_name):
        await self._init_session()
        async with self.session.get(f"{self.PYPI_JSON}/{package_name}/json") as response:
            if response.status == 200:
                return await response.json()
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
            info = await self._get_package_info(package_name)
            if not info:
                print(f"Package {package_name} not found")
                return
            
            if version:
                if version not in info['releases']:
                    print(f"Version {version} not found for {package_name}")
                    return
                target_version = version
            else:
                versions = sorted(info['releases'].keys(), key=version.parse)
                target_version = versions[-1] if latest else versions[-1]
            
            release = info['releases'][target_version][0]
            filename = release['filename']
            url = release['url'].replace("https://pypi.org", self.PYPI_MIRROR)
            
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
                        tar.extractall(install_dir)
                elif filename.endswith('.zip'):
                    with zipfile.ZipFile(filename) as zip_file:
                        zip_file.extractall(install_dir)
                
                # 安装包文件
                for item in install_dir.glob('**/*.py'):
                    if item.parent.name == 'site-packages':
                        continue
                    dest = self.site_packages / item.relative_to(install_dir)
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(item, dest)
                
                # 复制dist-info
                dist_info = next(install_dir.glob('*.dist-info'), None)
                if dist_info:
                    dest_info = self.site_packages / dist_info.name
                    if dest_info.exists():
                        shutil.rmtree(dest_info)
                    shutil.copytree(dist_info, dest_info)
                
                print(f"Successfully installed {package_name} {target_version}")
            finally:
                # 清理临时文件
                shutil.rmtree(install_dir)
                if os.path.exists(filename):
                    os.remove(filename)
        
        asyncio.run(_install())
    
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
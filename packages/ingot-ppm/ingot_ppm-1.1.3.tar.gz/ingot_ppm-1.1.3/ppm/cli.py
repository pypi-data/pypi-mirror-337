import click
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console
from . import __version__
from .core import PackageManager

console = Console()

@click.group()
def main():
    """PPM - A faster and more comprehensive Python package manager"""
    pass

@main.command()
@click.argument('package_name')
@click.option('-n', '--latest', is_flag=True, help='Install the latest version')
@click.option('-v', '--version', help='Install specific version')
def add(package_name, latest, version):
    """Install a Python package"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Installing {package_name}...", total=None)
        pm = PackageManager()
        pm.install_package(package_name, latest=latest, version=version)

@main.command()
def list():
    """List all installed packages"""
    pm = PackageManager()
    packages = pm.list_packages()
    for pkg in packages:
        console.print(f"{pkg.name} {pkg.version}")

@main.command()
@click.argument('package_name')
def info(package_name):
    """Show package information"""
    async def _show_info():
        pm = PackageManager()
        info = await pm._get_package_info(package_name)
        if info:
            console.print(f"[bold]包名:[/bold] {info['info']['name']}")
            console.print(f"[bold]当前版本:[/bold] {info['info']['version']}")
            console.print(f"[bold]作者:[/bold] {info['info']['author']}")
            console.print(f"[bold]描述:[/bold] {info['info']['summary']}")
            console.print(f"[bold]主页:[/bold] {info['info']['home_page']}")
            console.print(f"[bold]许可证:[/bold] {info['info']['license']}")
        else:
            console.print(f"未找到包 {package_name} 的信息")
    
    asyncio.run(_show_info())

@main.command()
@click.argument('package_name')
def remove(package_name):
    """Uninstall a package"""
    pm = PackageManager()
    site_packages = Path(sys.prefix) / "Lib" / "site-packages"
    dist_info = next(site_packages.glob(f"{package_name}-*.dist-info"), None)
    
    if not dist_info:
        console.print(f"未找到包 {package_name}")
        return
    
    try:
        # 删除包文件
        pkg_files = site_packages / package_name
        if pkg_files.exists():
            shutil.rmtree(pkg_files)
        
        # 删除dist-info
        shutil.rmtree(dist_info)
        console.print(f"成功卸载 {package_name}")
    except Exception as e:
        console.print(f"卸载失败: {str(e)}")

@main.command()
def update():
    """Update PPM and packages"""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="正在检查更新...", total=None)
        pm = PackageManager()
        pm.update_self()
        pm.update_package_list()

if __name__ == '__main__':
    main()
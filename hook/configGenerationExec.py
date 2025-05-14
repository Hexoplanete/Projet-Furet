import os
import glob

hiddenimports = []

# 1. Inclure tous les départements (modules Python dans chaque région)
regions_base_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'furet', 'crawler', 'regions')
for region in os.listdir(regions_base_path):
    region_path = os.path.join(regions_base_path, region)
    if os.path.isdir(region_path):
        init_path = os.path.join(region_path, '__init__.py')
        if not os.path.exists(init_path):
            continue  # skip namespace-style packages
        py_files = glob.glob(os.path.join(region_path, '*.py'))
        for file_path in py_files:
            filename = os.path.basename(file_path)
            if filename == '__init__.py':
                continue
            module_name = filename.replace('.py', '')
            full_import = f"furet.crawler.regions.{region}.{module_name}"
            hiddenimports.append(full_import)

# 2. Ajouter furet.crawler.spider s’il existe
spider_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'furet', 'crawler', 'spider.py')
if os.path.exists(spider_path):
    hiddenimports.append("furet.crawler.spider")

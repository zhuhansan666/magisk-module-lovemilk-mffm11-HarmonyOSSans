from pathlib import Path
from subprocess import run

input_dir = Path('mffm11_v2024.04.04_HarmonyOSSans/')
output = Path('./dist/mffm11_v2024.04.04_HarmonyOSSans.zip')

def get_version():
    with (input_dir / 'module.prop').open('r', encoding='u8') as fp:
        while line := fp.readline():
            if not line.startswith('version='):
                continue

            data = line.split('=', 1)[1].strip()
            return data.split('-', 1)[0] if '-' in data else data

def build():
    output.unlink(missing_ok=True)

    process = run([
        '7z',
        'a',
        str(output.absolute()),
        f'{str(input_dir.absolute())}/*',
    ])
    assert process.returncode == 0, 'failed to create zip file'

def release():
    version = get_version()
    process = run(f'gh release create V{version} --title "V{version}" --notes "" {output.absolute()}')

    assert process.returncode == 0, 'failed to create release'

if __name__ == '__main__':
    build()
    release()

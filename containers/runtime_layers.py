"""Split runtime files into bounded COPY layers without dereferencing package links."""
import os
from pathlib import Path
import shutil


def stage_layers(source, destination, limit=2*1024**3):
    if destination.exists(): shutil.rmtree(destination)
    destination.mkdir()
    index, size = 0, 0
    layers = []
    for root, directories, files in os.walk(source, followlinks=False):
        directories.sort()
        # os.walk reports symlinks to directories separately from regular files.
        links = [name for name in directories if (Path(root)/name).is_symlink()]
        for name in sorted(files+links):
            path = Path(root)/name
            count = 0 if path.is_symlink() else path.stat().st_size
            if count > limit: raise ValueError('Runtime file exceeds layer budget: '+str(path))
            if layers and size+count > limit:
                index += 1
                size = 0
            layer = destination/f'{index:04}'
            if not layer.exists():
                layer.mkdir()
                layers.append(layer)
            target = layer/path.relative_to(source)
            target.parent.mkdir(parents=True, exist_ok=True)
            if path.is_symlink():
                if not path.resolve().is_relative_to(source.resolve()):
                    raise ValueError('Runtime link escapes staging: '+str(path))
                target.symlink_to(os.readlink(path))
            else:
                os.link(path, target)
            size += count
    return layers

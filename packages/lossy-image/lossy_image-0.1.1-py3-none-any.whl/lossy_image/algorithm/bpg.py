import io
import os
import subprocess
from tempfile import NamedTemporaryFile

from PIL import Image
from lossy_image.algorithm import Algorithm

BPGENC_EXEC = os.getenv('BPGENC_EXEC', 'bpgenc')
BPGDEC_EXEC = os.getenv('BPGENC_EXEC', 'bpgdec')


class BpgAlgorithm(Algorithm):

    def __init__(self, **properties):
        super().__init__(**properties)
        self.quality = properties.get('quality', 30)
        self.subsampling = properties.get('subsampling', '420')
        self.bit_depth = properties.get('bit_depth', 8)
        self.color_space = properties.get('color_space', 'ycbcr')
        self.quantizer_parameter = properties.get('quantizer_parameter', 29)
        self.compression_level = properties.get('compression_level', 8)

    @property
    def name(self) -> str:
        return 'BPG'

    @staticmethod
    def _read(bpg_path):
        result = subprocess.run(
            [BPGDEC_EXEC, '-o', '-', bpg_path],
            stdout=subprocess.PIPE,
            check=True
        )
        return Image.open(io.BytesIO(result.stdout))

    def compress(self, image: Image.Image) -> Image.Image:
        with (NamedTemporaryFile(suffix='.png') as tmp_input,
              NamedTemporaryFile(suffix='.bpg') as tmp_output):
            image.save(tmp_input.name, format='PNG')
            subprocess.run([
                BPGENC_EXEC,
                '-o', tmp_output.name,
                '-q', str(self.quality),
                '-f', str(self.subsampling),
                '-c', self.color_space,
                '-b', str(self.bit_depth),
                '-q', str(self.quantizer_parameter),
                '-m', str(self.compression_level),
                tmp_input.name
            ], check=True)
            return self._read(tmp_output.name)

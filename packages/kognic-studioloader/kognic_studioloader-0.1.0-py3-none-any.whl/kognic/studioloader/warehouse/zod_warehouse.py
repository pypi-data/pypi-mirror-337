import logging
import glob
from pathlib import Path
import tempfile


try:
    from zod.cli.utils import SubDataset
    from zod.cli.download import DownloadSettings, FilterSettings
    from zod.constants import Version as VersionLiteral
    from zod.zod_sequences import ZodSequence, ZodSequences
    from zod.cli.download import _download_dataset
    from zod.cli.utils import Version
except ImportError as ie:
    print("Install with optional dependency [zod] for zod support")
    exit(1)


from kognic.studioloader.interfaces.loader import Loader
from kognic.studioloader.interfaces.warehouse import Warehouse
from kognic.studioloader.loader.zod_loader import ZodLoader

log = logging.getLogger(__name__)


class ZodWarehouse(Warehouse):
    def __init__(
        self,
        path: Path | None = None,
        version: VersionLiteral = "mini",
        bootstrap: bool = False,
        download_settings: DownloadSettings | None = None,
        filter_settings: FilterSettings | None = None,
    ):
        if path is None and not bootstrap:
            raise Exception(
                "Either provide a path where the dataset is downloaded, or run with bootstrap=True download the data"
            )

        if bootstrap:
            log.info(f"Will bootstrap zod dataset: {version}")
            temp_dir = Path(tempfile.gettempdir())
            existing_bootstrap_dirs = glob.glob(str(temp_dir / "zod_bootstrap_*"))
            if existing_bootstrap_dirs:
                log.info(
                    f"Found existing zod dataset already, will reuse: {existing_bootstrap_dirs[0]}"
                )
                self.path = existing_bootstrap_dirs[0]
            else:
                self.path = Path(tempfile.mkdtemp(prefix="zod_bootstrap_"))
                log.info(f"Will download dataset to: {self.path}")

            download_settings = download_settings or DownloadSettings(
                url="https://www.dropbox.com/sh/04dfm3npbwg5vpj/AAAVKmFIO0VClMFVy7qiRdQQa",
                output_dir=str(self.path),
                rm=False,
                dry_run=False,
                extract=True,
                extract_already_downloaded=False,
                parallel=True,
                max_workers=8,
            )

            filter_settings = filter_settings or FilterSettings(
                version=Version(version),
                annotations=True,
                images=True,
                blur=True,
                dnat=False,
                lidar=True,
                oxts=True,
                infos=True,
                vehicle_data=True,
                num_scans_before=0,
                num_scans_after=0,
            )
            _download_dataset(download_settings, filter_settings, SubDataset.SEQUENCES.folder)

        else:
            self.path = path

        self.sequences = ZodSequences(str(self.path), version)

    def get_available_scenes(self) -> list[str]:
        return list(self.sequences.get_all_ids())

    def initialize_scene(self, scene: str) -> Loader:
        sequence: ZodSequence = self.sequences[scene]
        return ZodLoader(sequence)

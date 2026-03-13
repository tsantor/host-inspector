from host_inspector.display.application.dtos import DisplayCollectionDTO
from host_inspector.display.application.dtos import DisplayInfoDTO


class LinuxDisplayCollector:
    def display_info(self) -> DisplayCollectionDTO:
        return DisplayCollectionDTO(
            items=[
                DisplayInfoDTO(
                    name="--",
                    display_id=1,
                    resolution_actual="--",
                    resolution="--",
                    refresh_rate="--",
                )
            ]
        )

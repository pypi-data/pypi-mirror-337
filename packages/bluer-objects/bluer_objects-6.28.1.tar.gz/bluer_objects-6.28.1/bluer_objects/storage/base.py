from bluer_objects.logger import logger


class StorageInterface:
    def download(
        self,
        object_name: str,
        filename: str = "",
        log: bool = True,
    ) -> bool:
        if log:
            logger.info(
                "{}.download {}{}".format(
                    self.__class__.__name__,
                    object_name,
                    f"/{filename}" if filename else "",
                )
            )

        return True

    def upload(
        self,
        object_name: str,
        filename: str = "",
        log: bool = True,
    ) -> bool:
        if log:
            logger.info(
                "{}.upload {}{}".format(
                    self.__class__.__name__,
                    object_name,
                    f"/{filename}" if filename else "",
                )
            )

        return True

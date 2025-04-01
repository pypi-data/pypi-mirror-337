from nsanic.libs.mult_log import NLogger


class LogMeta:

    @classmethod
    def logerr(cls, *err: str):
        NLogger.error(*err)

    @classmethod
    def loginfo(cls, *info):
        NLogger.info(*info)


class ConfMeta(LogMeta):

    conf = None

    @classmethod
    def set_conf(cls, conf):
        cls.conf = conf

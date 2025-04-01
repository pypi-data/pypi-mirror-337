from codemod.abc import BaseCodemod, BaseConfig


class MyCodemod(BaseCodemod[BaseConfig]):
    NAME = "my-codemod"

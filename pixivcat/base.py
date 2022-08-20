from typing import Dict

class BaseClient:
    pass


class BaseModel:
    def __init__(self, **kwds) -> None:
        for _k, _v in self.__annotations__.items():
            val = kwds.get(_k, None)
            if not val:
                val = None
            elif not isinstance(val, _v):
                val = _v(**val) if isinstance(val, Dict) else _v(*val)
            setattr(self, _k, val)

    def __str__(self) -> str:
        return "<"+self.__class__.__name__+":\n"+"".join([f"\t| {_k}: {_v}\n" for _k, _v in self.__dict__.items() if _v])+"\n>"


class MultiMediaBaseModel:
    def __init__(self, client: BaseClient, **kwds) -> None:
        self.client = client
        self.next_url = kwds.pop("next_url", None)
        for k, v in kwds.items():
            setattr(self, k, v)

    async def next(self):
        if self.next_url:
            response = await self.client.request("GET", self.next_url)
            return self.__class__(client=self.client, resp=response)
        return None

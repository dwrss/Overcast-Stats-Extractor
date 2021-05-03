from typing import MutableMapping


class NoCache(Exception):
    def __init__(self, *args: object) -> None:
        self.message = "No cached data found"
        super().__init__(*args)

    def __repr__(self) -> str:
        return "{class_full_name}({message})".format(class_full_name=self.__class__, message=self.message)

    def __str__(self) -> str:
        return "{class_name}:{message}".format(class_name=self.__class__.__name__, message=self.message)


class RequestError(Exception):
    def __init__(
        self, status_code: int, response_text: str, response_headers: MutableMapping
    ) -> None:
        self.status_code = status_code
        self.response_text = response_text
        self.response_headers = response_headers
        super().__init__()

    def __repr__(self) -> str:
        return "{class_name}({class_dict})".format(class_name=self.__class__, class_dict=self.__dict__)


class AuthenticationFailed(RequestError):
    def __str__(self) -> str:
        return (
            "Authentication failed with code '{code}' and message '{response}'".format(
                code=self.status_code, response=self.response_text
            )
        )


class OpmlFetchError(RequestError):
    def __str__(self) -> str:
        return "Failed to fetch Overcast Extended OMPL with code '{code}' and message '{response}'".format(
            code=self.status_code, response=self.response_text
        )

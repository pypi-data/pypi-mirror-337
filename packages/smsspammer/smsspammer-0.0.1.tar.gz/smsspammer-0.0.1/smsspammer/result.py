from dataclasses import dataclass


@dataclass(slots=True)
class Result:
    serviceName: str
    statusCode: int
    type: str

    def __repr__(self):
        return f"{self.type}->{self.serviceName}: {self.statusCode}"

    def __str__(self):
        return f"{self.type}->{self.serviceName}: {self.statusCode}"

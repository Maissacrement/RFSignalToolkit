import magpylib as mag3

class Analyse():
    def __init__(self) -> None:
        self.dataset = []
        src1 = mag3.magnet.Box(magnetization=(0,0,1000), dimension=(1,2,3))
        print(src1.__dict__)


analyser=Analyse()
print(analyser.dataset)
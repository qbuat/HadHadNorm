import ROOT
import uuid


class Data(object):
    
    def __init__(self):
        """
        """

        self._real     = ROOT.TH2F("hreal_" + uuid.uuid4().hex, "hreal", 10, 0, 1, 10, 0, 1)
        self._realfake = ROOT.TH2F("hrealfake_" + uuid.uuid4().hex, "hrealfake", 10, 0, 1, 10, 0, 1)
        self._fakefake = ROOT.TH2F("hfakefake_"+ uuid.uuid4().hex, "hfakefake", 10, 0, 1, 10, 0, 1)

        self._real.Sumw2()
        self._realfake.Sumw2()
        self._fakefake.Sumw2()

        self._real.GetXaxis().SetTitle('#tau_{1} BDT Score')
        self._real.GetYaxis().SetTitle('#tau_{2} BDT Score')
        self._realfake.GetXaxis().SetTitle('#tau_{1} BDT Score')
        self._realfake.GetYaxis().SetTitle('#tau_{2} BDT Score')
        self._fakefake.GetXaxis().SetTitle('#tau_{1} BDT Score')
        self._fakefake.GetYaxis().SetTitle('#tau_{2} BDT Score')

    @property
    def real(self):
        return self._real

    @property
    def realfake(self):
        return self._realfake

    @property
    def fakefake(self):
        return self._fakefake

    def create_templates(self, n_real=20000, n_realfake=20000, n_fakefake=20000):
        
        freal = ROOT.TF2("freal", "[0] * x *y", 0, 1, 0, 1)
        freal.SetParameter(0, 1)
#         freal.SetParameter(0, 1.2)

        ffake = ROOT.TF2("ffake", "[0] - [0] * x * y", 0, 1, 0, 1)
        ffake.SetParameter(0, 1)
#         ffake.SetParameter(0, 2)

        frealfake = ROOT.TF2("frealfake", " [0] * x + [1] * y", 0, 1, 0, 1)
        frealfake.SetParameter(0, 1)
        frealfake.SetParameter(0, 2)

        self._real.Reset()
        self._realfake.Reset()
        self._fakefake.Reset()

        self._real.FillRandom("freal", n_real)
        self._fakefake.FillRandom("ffake", n_fakefake)
        self._realfake.FillRandom("frealfake", n_realfake)

#         self._real.Scale(1. / self._real.Integral())
#         self._realfake.Scale(1. / self._realfake.Integral())
#         self._fakefake.Scale(1. / self._fakefake.Integral())

    def make_pseudo_data(self):
        h_d = self._real.Clone('h_pseudodata')
        h_d.Reset()
        h_d.Add(self._real)
        h_d.Add(self._fakefake)
        h_d.Add(self._realfake)
        return h_d

    def plot(self):
        plot = ROOT.TCanvas('data', 'data')
        plot.Divide(2, 2)
        plot.cd(1)
        self._real.Draw('colz')
        plot.cd(2)
        self._realfake.Draw('colz')
        plot.cd(3)
        self._fakefake.Draw('colz')
        plot.SaveAs('dump/input.pdf')

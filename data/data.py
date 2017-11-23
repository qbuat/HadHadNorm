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
        plot = ROOT.TCanvas('data', 'data', 1200, 400)
        plot.Divide(3, 1)
        pad = plot.cd(1)
        self._real.Draw('colz')
        ttext_1 = ROOT.TLatex(
            pad.GetLeftMargin() + 0.01,
            1 - pad.GetTopMargin() + 0.02, 
            "Z#rightarrow#tau#tau")
        ttext_1.SetNDC(True)
        ttext_1.SetTextSize(15)
        ttext_1.Draw()

        pad = plot.cd(2)
        self._realfake.Draw('colz')
        ttext_2 = ROOT.TLatex(
            pad.GetLeftMargin() + 0.01,
            1 - pad.GetTopMargin() + 0.02, 
            "Others")
        ttext_2.SetNDC(True)
        ttext_2.SetTextSize(15)
        ttext_2.Draw()

        pad = plot.cd(3)
        self._fakefake.Draw('colz')
        self._realfake.Draw('colz')
        ttext_3 = ROOT.TLatex(
            pad.GetLeftMargin() + 0.01,
            1 - pad.GetTopMargin() + 0.02, 
            "Fake")
        ttext_3.SetNDC(True)
        ttext_3.SetTextSize(15)
        ttext_3.Draw()
        plot.SaveAs('dump/input.pdf')

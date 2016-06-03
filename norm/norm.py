import ROOT
import uuid

class norm_fitter(object):

    def __init__(self, h_data, h_real, h_realfake, h_fakefake):
        
        self.tau1_score = ROOT.RooRealVar(
            "tau1_score", "#tau_{1} BDT Score", 0, 1)
        self.tau2_score = ROOT.RooRealVar(
            "tau2_score", "#tau_{2} BDT Score", 0, 1)

        ## input data
        self.data = ROOT.RooDataHist(
            'data', 'data', ROOT.RooArgList(
                self.tau1_score, self.tau2_score), h_data)

        ## real pdf
        self.real = ROOT.RooDataHist(
            'real', 'real', ROOT.RooArgList(
                self.tau1_score, self.tau2_score), h_real)
        self.real_pdf = ROOT.RooHistPdf(
            'real_pdf', 'real_pdf', ROOT.RooArgSet(
                self.tau1_score, self.tau2_score), self.real)

        ## real fake pdf
        self.realfake = ROOT.RooDataHist(
            'realfake', 'realfake', ROOT.RooArgList(
                self.tau1_score, self.tau2_score), h_realfake)
        self.realfake_pdf = ROOT.RooHistPdf(
            'realfake_pdf', 'realfake_pdf', ROOT.RooArgSet(
                self.tau1_score, self.tau2_score), self.realfake)

        ## fake fake pdf
        self.fakefake = ROOT.RooDataHist(
            'fakefake', 'fakefake', ROOT.RooArgList(
                self.tau1_score, self.tau2_score), h_fakefake)
        self.fakefake_pdf = ROOT.RooHistPdf(
            'fakefake_pdf', 'fakefake_pdf', ROOT.RooArgSet(
                self.tau1_score, self.tau2_score), self.fakefake)

        ## yields to extract
        self.nreal = ROOT.RooRealVar(
            "n_real", "n_real", 
            h_data.Integral() / 3,
            0, h_data.Integral())
        
        self.nrealfake = ROOT.RooRealVar(
            "n_realfake", "n_realfake", 
            h_data.Integral() / 3,
            0, h_data.Integral())

        self.nfakefake = ROOT.RooRealVar(
            "n_fakefake", "n_fakefake", 
            h_data.Integral() / 3,
            0, h_data.Integral())
        
        ## Full model to fit to the data
        self.model = ROOT.RooAddPdf(
            'model', 'model', 
            ROOT.RooArgList(
                self.real_pdf, self.realfake_pdf, self.fakefake_pdf),
            ROOT.RooArgList(
                self.nreal, self.nrealfake, self.nfakefake))
        ## fit res object
        self._fitres = None
                                         
    @property
    def n_real(self):
        return self.nreal.getVal()

    @property
    def n_real_err(self, assymetric=False):
        if assymetric:
            return (self.nreal.getErrorLo(), self.nreal.getErrorHi())
        else:
            return self.nreal.getError()

    @property
    def n_realfake(self):
        return self.nrealfake.getVal()

    @property
    def n_realfake_err(self, assymetric=False):
        if assymetric:
            return (self.nrealfake.getErrorLo(), self.nrealfake.getErrorHi())
        else:
            return self.nrealfake.getError()

    @property
    def n_fakefake(self):
        return self.nfakefake.getVal()

    @property
    def n_fakefake_err(self, assymetric=False):
        if assymetric:
            return (self.nfakefake.getErrorLo(), self.nfakefake.getErrorHi())
        else:
            return self.nfakefake.getError()

    def fit(self, constant_others=False):
        if constant_others:
            print self.realfake.sum(True)
            self.nrealfake.setVal(self.realfake.sum(True))
            self.nrealfake.setConstant(True)

        self._fitres = self.model.fitTo(
            self.data, ROOT.RooFit.Extended(True),
            ROOT.RooFit.Save(True))

    @property
    def fitres(self):
        return self._fitres

    def integral_z(tau1_score_cut, tau2_score_cut):
        return 1
    

    def frame(self, var='tau1_score'):
        """
        """
        plot = getattr(self, var).frame(0, 1, 10)
        plot.SetName('tau1_score')

        self.data.plotOn(
            plot, ROOT.RooFit.Name('Data'),
            ROOT.RooFit.LineColor(ROOT.kBlack),
            ROOT.RooFit.MarkerColor(ROOT.kBlack))

        self.model.plotOn(
            plot, ROOT.RooFit.Name('Total'),
            ROOT.RooFit.LineColor(ROOT.kBlack),
            ROOT.RooFit.LineStyle(ROOT.kSolid))

        self.model.plotOn(
            plot, ROOT.RooFit.Name('Z#rightarrow#tau#tau'),
            ROOT.RooFit.LineColor(ROOT.kBlue),
            ROOT.RooFit.LineStyle(ROOT.kDashed),
            ROOT.RooFit.Components(self.real_pdf.GetName()))

        self.model.plotOn(
            plot, ROOT.RooFit.Name('Fakes'),
            ROOT.RooFit.LineColor(ROOT.kGreen),
            ROOT.RooFit.LineStyle(ROOT.kDashed),
            ROOT.RooFit.Components(self.fakefake_pdf.GetName()))

        self.model.plotOn(
            plot, ROOT.RooFit.Name('Others'),
            ROOT.RooFit.LineColor(ROOT.kRed),
            ROOT.RooFit.LineStyle(ROOT.kDashed),
            ROOT.RooFit.FillStyle(0),
            ROOT.RooFit.Components(self.realfake_pdf.GetName()))

        return plot



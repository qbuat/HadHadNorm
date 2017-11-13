import uuid
import ROOT

def decorated_plot(
    roo_plot,
    pad_x=650, pad_y=600,
    model='Total', 
    data='Data',
    ndof=3 - 1,#extended fit
    legend_position='right'):

    pad = ROOT.TCanvas(
        'pad_' + uuid.uuid4().hex,
        roo_plot.GetXaxis().GetTitle(), 
        pad_x, pad_y)

    roo_plot.SetMaximum(1.05 * roo_plot.GetMaximum())
    roo_plot.Draw()
    label = ROOT.TLatex(
        pad.GetLeftMargin(),
        1 - pad.GetTopMargin() + 0.015,
        '#chi^{{2}}/dof = {0:1.3f}'.format(
            roo_plot.chiSquare(model, data, ndof)))
    label.SetNDC(True)
    label.SetTextSize(20)
    label.Draw()
            
    plotables = [
        roo_plot.getObject(idx) for idx in xrange(int(roo_plot.numItems()))
        ]

    hists = filter(lambda h: isinstance(h, ROOT.RooHist), plotables)
    curves = filter(lambda h: isinstance(h, ROOT.RooCurve), plotables)

    legend = ROOT.TLegend(
        pad.GetLeftMargin() + 0.01, 1 - pad.GetTopMargin() - 0.06,
        1 - pad.GetRightMargin(), 1 - pad.GetTopMargin() - 0.01)
    for hist in hists:
        legend.AddEntry(hist, hist.GetName(), 'lep')
    legend.SetTextSize(20)
    for curve in curves:
        legend.AddEntry(curve, curve.GetName(), 'l')
    legend.SetNColumns(len(hists) + len(curves))
    legend.Draw()
    pad.RedrawAxis()
    return pad

def get_response_graph(
    frac_range,
    name=uuid.uuid4().hex,
    title='Z#rightarrow#tau#tau',
    color=ROOT.kBlue):
    graph = ROOT.TGraphErrors(len(frac_range))
    graph.SetName(name)
    graph.SetTitle(title)
    graph.SetFillColor(color)
    graph.SetLineColor(color)
    graph.SetMarkerColor(color)
    graph.SetFillStyle(0)
    graph.SetMarkerSize(0.1)
    return graph


def response_plot(gr_z, gr_fakes):
    c_resp = ROOT.TCanvas()
    h_template = ROOT.TH1F(uuid.uuid4().hex, 'response', 10, 0, 100)
    h_template.GetXaxis().SetTitle('Fraction of Injected Z#rightarrow#tau#tau (%)')
    h_template.GetYaxis().SetTitle('N(fitted) / N(injected)')
    h_template.GetXaxis().SetRangeUser(0, 100)
    h_template.GetYaxis().SetRangeUser(0.4, 1.6)
    h_template.Draw('HIST')
    line = ROOT.TLine(0, 1, 100, 1)
    line.Draw()
    
    gr_z.Draw('SAMEPE5')
    gr_fakes.Draw('SAMEPE5')
    legend = ROOT.TLegend(
        0.8, 1 - c_resp.GetTopMargin() - 0.2,
        1 - c_resp.GetRightMargin(), 1 - c_resp.GetTopMargin() - 0.05)
    legend.AddEntry(gr_z, gr_z.GetTitle(), 'fp')
    legend.AddEntry(gr_fakes, gr_fakes.GetTitle(), 'fp')
    legend.SetTextSize(20)
    legend.Draw()
    c_resp.RedrawAxis()
    return c_resp

def yields_plot(fit_z, fit_fakes, exp_z, exp_fakes, ntot):
    c_resp = ROOT.TCanvas()
    h_template = ROOT.TH1F(uuid.uuid4().hex, 'response', 10, 0, 100)
    h_template.GetXaxis().SetTitle('Fraction of Injected Z#rightarrow#tau#tau (%)')
    h_template.GetYaxis().SetTitle('Yields')
    h_template.GetXaxis().SetRangeUser(0, 100)
    h_template.GetYaxis().SetRangeUser(0., ntot)
    h_template.Draw('HIST')
    
    ROOT.TGraph(exp_z).Draw('SAMEL')
    ROOT.TGraph(exp_fakes).Draw('SAMEL')
    fit_z.Draw('SAMEPE')
    fit_fakes.Draw('SAMEPE')


    legend = ROOT.TLegend(
        0.4, 1 - c_resp.GetTopMargin() - 0.15,
        1 - c_resp.GetRightMargin() - 0.1, 1 - c_resp.GetTopMargin() - 0.01)
    legend.SetNColumns(2)
    legend.AddEntry(exp_z, 'Exp. ' + exp_z.GetTitle(), 'l')
    legend.AddEntry(fit_z, 'Fitted ' + fit_z.GetTitle(), 'lp')
    legend.AddEntry(exp_fakes, 'Exp. ' + exp_fakes.GetTitle(), 'l')
    legend.AddEntry(fit_fakes, 'Fitted ' + fit_fakes.GetTitle(), 'lp')
    legend.SetTextSize(15)
    legend.Draw()
    c_resp.RedrawAxis()
    return c_resp

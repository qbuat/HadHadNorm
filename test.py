import ROOT
from rootpy.plotting.style import set_style
from data import Data
from norm.norm import norm_fitter
from norm.utils import get_response_graph, response_plot, yields_plot, decorated_plot


# Create templates from pseudo data
N = int(2e6)
template = Data()
template.create_templates(
    n_real=N, n_realfake=N, n_fakefake=N)
set_style('ATLAS', shape='square')
template.plot()

# Toy study based on ntot events
ntot = 10000
n_others = 1000
step = 2
my_frac_range = range(10, 90, step)
res_z = get_response_graph(my_frac_range)
res_fakes = get_response_graph(my_frac_range, title='Fakes', color=ROOT.kGreen)
yields_fitted_z = get_response_graph(my_frac_range)
yields_fitted_fakes = get_response_graph(my_frac_range, title='Fakes', color=ROOT.kGreen)
yields_exp_z = get_response_graph(my_frac_range)
yields_exp_fakes = get_response_graph(my_frac_range, title='Fakes', color=ROOT.kGreen)

for ip, frac in enumerate(my_frac_range):
    n_z = int(float(frac) / 100. * (ntot - n_others))
    n_fakes = ntot - n_z - n_others
    pseudo_data = Data()
    pseudo_data.create_templates(
    n_real=n_z,
    n_realfake=n_others, 
    n_fakefake=n_fakes)
    h_pseudo_data = pseudo_data.make_pseudo_data()
    print 'total data = ', h_pseudo_data.Integral()
    fitter = norm_fitter(h_pseudo_data, template.real, template.realfake, template.fakefake)
    fitter.fit(constant_others=False)
    print fitter.fitres
    fitter.fitres.Print('v')
    print fitter.n_real, fitter.n_real_err, '/', n_z
    res_z.SetPoint(ip, float(frac), fitter.n_real / n_z)
    res_z.SetPointError(ip, float(step) / 2., fitter.n_real_err / n_z)
    res_fakes.SetPoint(ip, float(frac), fitter.n_fakefake / n_fakes)
    res_fakes.SetPointError(ip, float(step) / 2., fitter.n_fakefake_err / n_fakes)
    yields_fitted_z.SetPoint(ip, float(frac), fitter.n_real)
    yields_fitted_z.SetPointError(ip, float(step) / 2., fitter.n_real_err)
    yields_fitted_fakes.SetPoint(ip, float(frac), fitter.n_fakefake)
    yields_fitted_fakes.SetPointError(ip, float(step) / 2., fitter.n_fakefake_err)
    yields_exp_z.SetPoint(ip, float(frac), n_z)
    yields_exp_z.SetPointError(ip, float(step) / 2., 0)
    yields_exp_fakes.SetPoint(ip, float(frac), n_fakes)
    yields_exp_fakes.SetPointError(ip, float(step) / 2., 0)

c_resp = response_plot(res_z, res_fakes)
c_resp.Update()
c_resp.SaveAs('dump/response.pdf')

c_yields = yields_plot(
    yields_fitted_z, yields_fitted_fakes,
    yields_exp_z, yields_exp_fakes, ntot)
c_yields.Update()    
c_yields.SaveAs('dump/yields.pdf')

# For now it's pseudo data
n_real_target = 10000
n_realfake_target = 20000
n_fakefake_target = 50000

data = Data()
data.create_templates(
    n_real=n_real_target, 
    n_realfake=n_realfake_target, 
    n_fakefake=n_fakefake_target)
h_data = data.make_pseudo_data()




Fit = norm_fitter(h_data, template.real, template.realfake, template.fakefake)
res = Fit.fit(constant_others=True)
fitter.fitres.Print('v')
print Fit.n_real, Fit.n_real_err, n_real_target
print Fit.n_realfake, Fit.n_realfake_err, n_realfake_target
print Fit.n_fakefake, Fit.n_fakefake_err, n_fakefake_target

plot1 = Fit.frame('tau1_score')
plot2 = Fit.frame('tau2_score')

pad1 = decorated_plot(plot1)
pad1.Update()
pad1.SaveAs('dump/2dfit_tau1_score.pdf')

pad2 = decorated_plot(plot2)
pad2.Update()
pad2.SaveAs('dump/2dfit_tau2_score.pdf')




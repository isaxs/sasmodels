static double form_volume(double radius)
{
    return sphere_volume(radius);
}

// TODO: remove Iq when Iqxy can use Fq directly
static double Iq(double q, double sld, double sld_solvent, double radius)
{
    return sphere_form(q, radius, sld, sld_solvent);
}

static void Fq(double q, double *F1,double *F2, double sld, double solvent_sld, double radius)
{
    const double fq = sas_3j1x_x(q*radius);
    const double contrast = (sld - solvent_sld);
    const double form = 1e-2 * contrast * sphere_volume(radius) * fq;
    *F1 = form;
    *F2 = form*form;
}
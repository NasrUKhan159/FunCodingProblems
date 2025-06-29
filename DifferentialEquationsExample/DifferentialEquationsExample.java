// Find solution of initial value problem using differential equation:
// $\frac{du(t)}{dt} + a(t)u(t)dt = f(t) ; 0 < t \leq T; u(0) = A$

// Interfaces for *Continuous* problem
interface IODE<V> { // V = underlying numeric type
    // u = u(t); du/dt + a(t)u = f(t)
    V a(V t); // Coefficient of free term
    V f(V t); // Inhomogeneous term
}

interface IIVP<V> { // Specify initial condition and range [0,T] of integration
    V getInitialCondition();
    void setInitialCondition(V value);
    V getExpiry();
    void setExpiry(V value);
}

// Interfaces for the *Discrete* problem
interface IFDM<V> { // V = underlying numeric type
    // Computation from a given time level n to the next time level n+1
    void calculateOneStep(int n); // One-step method
}

class ODE implements IIVP<Double> {
    private double A; // Initial condition
    private double T; // Solve in interval [0, T]

    public ODE(double InitCondition, double Expiry) {
        A = InitCondition;
        T = Expiry;
    }

    public double a(double t) { // Coefficient of free term
        return 1.0;
    }

    public double f(double t) { // Inhomogeneous term
        return 2.0 + t;
    }

    public Double getInitialCondition() {
        return A;
    }

    public void setInitialCondition(Double value) {
        A = value;
    }

    public Double getExpiry() {
        return T;
    }

    public void setExpiry(Double value) {
        T = value;
    }
}

abstract class OneStepFDM implements IFDM<Double> {
    protected int NSteps; // Number of time steps
    protected ODE ode; // The references to ODE

    protected double vOld, vNew; // Values at levels n, n+1
    protected double[] mesh;
    protected double delta_T; // Step length

    public OneStepFDM(int NSteps, ODE ode) {
        this.NSteps = NSteps;
        this.ode = ode;
        vOld = ode.getInitialCondition();
        vNew = vOld;
        mesh = new double[NSteps + 1];
        mesh[0] = 0.0;
        mesh[NSteps] = ode.getExpiry();
        delta_T = (mesh[NSteps] - mesh[0]) / NSteps;

        for (int n = 1; n < NSteps; n++) {
            mesh[n] = mesh[n - 1] + delta_T;
            System.out.printf(", %f", mesh[n]);
        }
    }

    public abstract void calculateOneStep(int m); // One-step method

    // The full algorithm computed at the expiry t = T
    public double calculate() {
        for (int m = 0; m <= NSteps; m++) {
            calculateOneStep(m);
            vOld = vNew;
        }
        return vNew;
    }

    public double getValue() { // Computed value
        return vNew;
    }
}

class ExplicitEuler extends OneStepFDM {
    public ExplicitEuler(int NSteps, ODE ode) {
        super(NSteps, ode);
    }

    public void calculateOneStep(int n) { // One-step method
        // Create temp vars for readability
        double aVar = ode.a(mesh[n]);
        double fVar = ode.f(mesh[n]);

        vNew = (1.0 - delta_T * aVar) * vOld + delta_T * fVar;
        System.out.printf("old, new: [%f, %f]%n", vOld, vNew);
    }
}

class TestIVP {
    public static void main(String[] args) {
        // experiment with different values of A, T, initial condition, expiry and N
        double A = 1.0;
        double T = 1.0;

        ODE myODE = new ODE(A, T);

        myODE.setInitialCondition(2.0);
        myODE.setExpiry(2.0);

        // Calculate the FD scheme
        int N = 100; // Number of steps

        ExplicitEuler myFDM = new ExplicitEuler(N, myODE);

        myFDM.calculate();
        double val = myFDM.getValue();
        System.out.printf("fdm value: %f%n", val);
    }
}
using GLMakie
using DifferentialEquations
using ParameterizedFunctions
using Formatting

fig = Figure(resolution=(800, 600))
ax = Axis(fig[1, 1], aspect=1)

lsgrid = SliderGrid(fig[1,2],
    (label = "Initial pos", range = -1:0.01:1, startvalue = 0, format = "{:.2f}m"),
    (label = "Initial vel", range = -1:0.01:10, startvalue = 0, format = "{:.2f}m/s"),
    (label = "Stiffness", range = 0:0.01:10, startvalue = 1, format = "{:.2f}Ns/m"),
    (label = "Damping", range = 0:0.01:10, startvalue = 0, format = "{:.2f}N/m"),
    (label = "Mass", range = 0.1:0.01:10, startvalue = 1, format = "{:.2f}kg"),
    (label = "Initial pos 2", range = -1:0.01:1, startvalue = 0, format = "{:.2f}m"),
    (label = "Initial vel 2", range = -1:0.01:1, startvalue = 0, format = "{:.2f}m/s"),
    (label = "Stiffness 2", range = 0:0.01:2, startvalue = 0.5, format = "{:.2f}Ns/m"),
    (label = "Damping 2", range = 0:0.0025:2, startvalue = 0.1, format = "{:.2f}N/m"),
    (label = "Mass 2", range = 0.1:0.0025:2, startvalue = 1, format = "{:.2f}kg"),
)

sliderobservables = [s.value for s in lsgrid.sliders]
x₀₁, v₀₁, k₁, c₁, m₁, x₀₂, v₀₂, k₂, c₂, m₂ = sliderobservables

odeSystem = @ode_def begin
    dx₁ = v₁
    dx₂ = v₂
    dv₁ = (-(k₁ + k₂) * x₁ - (c₁ + c₂) * v₁ + k₂ *  x₂ + c₂ * v₂) / m₁
    dv₂ = (k₂ * x₁ + c₂ * v₁ - k₂ * x₂ - c₂ * v₂) / m₂
end k₁ k₂ c₁ c₂ m₁ m₂
tspan = (0, 150)

points = @lift begin
    u₀ = [$x₀₁, $x₀₂, $v₀₁, $v₀₂]
    p = [$k₁, $k₂, $c₁, $c₂, $m₁, $m₂]
    prob = ODEProblem(odeSystem, u₀, tspan, p, reltol=1e-14, abstol=1e-14)
    sol = solve(prob, alg=Vern9())
    y = [x[1] for x in sol.u]
    t = sol.t
    Point2f.(t, y)
end

points2 = @lift begin
    u₀ = [$x₀₁, $x₀₂, $v₀₁, $v₀₂]
    p = [$k₁, $k₂, $c₁, $c₂, $m₁, $m₂]
    prob = ODEProblem(odeSystem, u₀, tspan, p, reltol=1e-14, abstol=1e-14)
    sol = solve(prob, alg=Vern9())
    y = [x[2] for x in sol.u]
    t = sol.t
    Point2f.(t, y)
end

lines!(points, linewidth=5)
lines!(points2)

display(fig)
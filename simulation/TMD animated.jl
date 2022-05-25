"""
Animates a TMD system over time using a system of ordinary differential equations
"""
using DifferentialEquations
using Plots
using ParameterizedFunctions

TMD! = @ode_def begin
  dx₁ = v₁
  dx₂ = v₂
  dv₁ = (-(k₁ + k₂) * x₁ - (c₁ + c₂) * v₁ + k₂ * x₂ + c₂ * v₂) / m₁
  dv₂ = (k₂ * x₁ + c₂ * v₁ - k₂ * x₂ - c₂ * v₂) / m₂
end k₁ k₂ c₁ c₂ m₁ m₂

u₀ = [1, 0, 0, 0] #Initial conditions, x₁, x₂, v₁, v₂
tspan = (0, 50) # span of simulation
p = (23, 11, 0, 0.2, 1, 1) #Paramters for simulation

prob = ODEProblem(TMD!, u₀, tspan, p, reltol=1e-9, abstol=1e-9)
sol = solve(prob)

x₁ = [x[1] for x in sol.u]
x₂ = [x[2] for x in sol.u]
v₁ = [x[3] for x in sol.u]
v₂ = [x[4] for x in sol.u]
dt = sol.t
n = length(sol.t)
df = 2 #Frames skipped per animation step, increase to speed up simulation at the expense of smoothness

anim = @animate for i = 1:df:n
  plot(dt[1:i], x₁[1:i], legend=false)
  plot!(dt[1:i], x₂[1:i], legend=false)
end

gif(anim, "spring.gif", fps=20)

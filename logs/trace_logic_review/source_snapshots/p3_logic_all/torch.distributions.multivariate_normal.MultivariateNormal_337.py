
loc = torch.tensor(torch.ones((2, 2)))
covariance = (torch.eye(2) - 0.5)
mvn = torch.distributions.multivariate_normal.MultivariateNormal(loc, covariance)
mv_normal = mvn.log_prob(torch.randn(2, 2, 2, 2)).mean(dim=0)

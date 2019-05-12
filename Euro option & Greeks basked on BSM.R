#This function only contain the results of vega,delta,gamma
s=50:150;  K=105;  K_p=95;  K_c=105;  sigma=0.2;  r=0.05; inte=1
#The following codes collaborate with risk management, it's helpful in figuring out delta, gamma, vega, payoff, value in Euro option. Others Greeks, rho for instance, are not available so far since I've not fully comprehended the approaches to derive them in mathematics(they do exist in our text book, however). Another reason is that those greeks accessible at present are sufficient for the case analysis since the collar option virtually not relys on Greeks but implied volatility.

greeks=function(s,K,sigma,r,inte,result,type)
{
  if(type=="call")
  {


    d1_c=(log(s/K)+（r+sigma^2/2)*(inte))/(sigma*sqrt(inte))
    d2_c=d1_c-sigma*sqrt(inte);
    N_d1_c=pnorm(d1_c,0,1)
    N_d2_c=pnorm(d2_c,0,1)
    
    if(result=="payoff")
    {
      payoff=NULL;
      for(i in 1:length(s))
      {
        payoff[i]=max(s[i]-K,0)
      }
      plot(s,payoff,type="l",main="payoff")

    }
    payoff

    if(result=="value")
    {
      c=s*N_d1_c - K*exp(1)^(-r*inte)*N_d2_c
      plot(s,c,type="l",main="value")

    }
    c

    if(result=="delta")
    {
      delta=N_d1_c
      plot(s,delta,type="l",main="delta")

    }
      delta

    if(result=="gamma")
    {
      gamma=(1/sqrt(2*pi)*exp(1)^(-d1_c^2/2))/(s*sigma*sqrt(inte))
      plot(s,gamma,type="l",main="gamma")
    }
      gamma

    if(result=="vega")
    {
      vega=s*sqrt(inte)*(1/sqrt(2*pi)*exp(1)^(-d1_c^2/2))
      plot(s,vega,type="l",main="vega")
    }
      vega


  }
  if(type=="put")
  {
    d1_p=(log(s/K_p)+（r+sigma^2/2)*(inte))/(sigma*sqrt(inte))
    d2_p=d1_p-sigma*sqrt(inte);
    N_d1_p=pnorm(-d1_p,0,1)
    N_d2_p=pnorm(-d2_p,0,1)

    if(result=="payoff")
    {
      payoff=NULL;
      for(i in 1:length(s))
      {
        payoff[i]=max(K-s[i],0)
      }
      plot(s,payoff,type="l",main="payoff")

    }
    payoff

    if(result=="value")
    {
      p=K*exp(1)^(-r*inte)*N_d2_p - s*N_d1_p
      plot(s,p,type="l",main="value")

    }
    p

    if(result=="delta")
    {
      delta=-N_d1_p
      plot(s,delta,type="l",main="delta")

    }
    delta

    if(result=="gamma")
    {
      gamma=(1/sqrt(2*pi)*exp(1)^(-d1_p^2/2))/(s*sigma*sqrt(inte))
      plot(s,gamma,type="l",main="gamma")
    }
    gamma

    if(result=="vega")
    {
      vega_p=s*sqrt(inte)*(1/sqrt(2*pi)*exp(1)^(-d1_p^2/2))
      plot(s,vega,type="l",main="vega")
    }
    vega

  }
}

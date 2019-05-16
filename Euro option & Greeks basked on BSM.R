#This function only contain the results of vega,delta,gamma
s=50:150;  K=51;  K_p=95;  K_c=105;  sigma=0.28;  r=0.06; inte=9/12
#The following codes collaborate with risk management, it's helpful in figuring out delta, gamma, vega, payoff, value in Euro option. Others Greeks, rho for instance, are not available so far since I've not fully comprehended the approaches to derive them in mathematics(they do exist in our text book, however). Another reason is that those greeks accessible at present are sufficient for the case analysis since the collar option virtually not relys on Greeks but implied volatility.

greeks=function(s,K,sigma,r,inte,result,ty)
{
  d1=(log(s/K)+(r+(sigma^2/2))*inte)/(sigma*sqrt(inte))
  d2=d1-sigma*sqrt(inte)
  #--------------------------
  if(result=="payoff")
  {
    if(ty=="call")
    {
      payoff=NA;
      for(i in 1:length(s))
      {
        payoff[i]=max(s[i]-K,0)
      }
      payoff
    }
    else if(ty=="put")
    {
      payoff=NA;
      for(i in 1:length(s))
      {
        payoff[i]=max(K-s[i],0)
      }
      payoff
    }
  }
  #-------------------------
  else if(result=="value")
  {
    if(ty=="call")
    {
      c=s*pnorm(d1,0,1)-K*exp(1)^(-r*inte)*pnorm(d2,0,1)
      c
    }
    else if(ty=="put")
    {
      p=K*exp(1)^(-r*inte)*pnorm(-d2,0,1)-s*pnorm(-d1,0,1)
      p
    }
  }
  #-----------------------
  else if(result=="delta")
  {
    if(ty=="call")
    {
      delta_c=pnorm(d1,0,1)
      delta_c
    }
    else if(ty=="put")
    {
      delta_p=pnorm(d1,0,1)-1
      delta_p
    }
  }
  #----------------------
  else if(result=="gamma")
  {
    if(ty=="call"| ty=="put")
    {
      gamma=(exp(1)^(-0.5*d1^2))/(s*sigma*sqrt(2*pi*inte))
      gamma
    }
  }
  #---------------------
  else if(result=="vega")
  {
    if(ty=="call"| ty=="put")
    {
      vega=s*sqrt(inte)*(exp(1)^(-d1^2/2))/sqrt(2*pi)
      vega
    }
  }
}

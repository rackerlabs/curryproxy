using System.Collections.Generic;

namespace Curry.Services
{
    public enum CurryConfigKeys
    {
        DEV,
        TEST,
        QA,
        PREPROD,
        PROD

    }
    public class CurryConfiguration
    {
        public Dictionary<string, string> curryConfig { get; set; }

        public CurryConfiguration()
        {
            curryConfig = new Dictionary<string, string>();
            curryConfig.Add(CurryConfigKeys.DEV.ToString() , "https://api.drivesrvr-dev.com");
            curryConfig.Add(CurryConfigKeys.TEST.ToString() , "https://testapi.drivesrvr-qa.com");
            curryConfig.Add(CurryConfigKeys.QA.ToString(), "https://controlpanelsvc.drivesrvr-qa.com");
            curryConfig.Add(CurryConfigKeys.PREPROD.ToString(), "https://ppapi.drivesrvr-staging.com");
            curryConfig.Add(CurryConfigKeys.PROD.ToString(), "https://api.drivesrvr.com");
      
        }

    }
}
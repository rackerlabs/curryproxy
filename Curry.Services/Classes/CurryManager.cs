using System;
using System.Web;
using System.Net;


namespace Curry.Services
{

    //This will wrap response code as well
    [Serializable]
    public class CurryRelayResponse
    {
        public HttpStatusCode httpStatusCode { get; set; }
        public string httpStatusDescription { get; set; }

        public object data { get; set; }
    }
    public class CurryManager
    {
        
        CurryRequestRelay curryRelay = new CurryRequestRelay();


        /// <summary>
        /// Relays Request to the actual API that is in a different data center
        /// </summary>
        /// <param name="env"></param>
        /// <param name="originalUrl"></param>
        /// <param name="currentReq"></param>
        /// <returns></returns>
        public CurryRelayResponse RelayRequest(string env, Uri originalUrl, HttpRequestBase currentReq)
        {
            string cacheKey = string.Empty;

            if (currentReq.Headers["X-Auth-Token"] != null)
            {
                cacheKey = string.Format("{1}", originalUrl.ToString(), currentReq.Headers["X-Auth-Token"]);

            }

            CurryRelayResponse objectInCache = (CurryRelayResponse) Curry.Services.Caching.CurryCache.Get(cacheKey);

            if (objectInCache != null)
            {
                return objectInCache;
            }

            //Else proceed to make the actual call

            CurryRelayResponse response = new CurryRelayResponse();

            CurryConfiguration config = new CurryConfiguration();

            string urlSegmentToReplace = string.Empty;
            string baseUrl = string.Empty;

            switch (env.ToLowerInvariant())
            {
                case "dev":
                    urlSegmentToReplace = "dev/";
                    baseUrl = config.curryConfig[CurryConfigKeys.DEV.ToString()];
                    break;
                case "test":
                    urlSegmentToReplace = "test/";

                    baseUrl = config.curryConfig[CurryConfigKeys.TEST.ToString()];
                    break;
                case "qa":
                    urlSegmentToReplace = "qa/";

                    baseUrl = config.curryConfig[CurryConfigKeys.QA.ToString()];
                    break;
                case "preprod":
                    urlSegmentToReplace = "preprod/";

                    baseUrl = config.curryConfig[CurryConfigKeys.PREPROD.ToString()];
                    break;
                case "prod":
                    urlSegmentToReplace = "prod/";

                    baseUrl = config.curryConfig[CurryConfigKeys.PROD.ToString()];
                    break;
            }

            string pathafter = originalUrl.PathAndQuery.Replace(urlSegmentToReplace, string.Empty).ToString();

            string relayUrl = baseUrl + pathafter;

            //wrap the response from other API server
            response.data = curryRelay.RelayRequest<object>(relayUrl, currentReq);
            response.httpStatusCode = curryRelay.HttpStatusCode;
            response.httpStatusDescription = curryRelay.HttpStatusDescription;

            //Insert in cache
            Curry.Services.Caching.CurryCache.Insert(cacheKey, response, new TimeSpan(0, 0, 30));

            return response;
        }
    }
}
using System;
using Enyim.Caching;
using Enyim.Caching.Memcached;
using System.Configuration;

namespace Curry.Services.Caching
{
    public static class CurryCache 
    {
        private static string RaxCachePrefix;
        private static TimeSpan ValidForTimeSpan;
        public static MemcachedClient client;


        /// <summary>
        /// internal constructor
        /// </summary>
        static CurryCache()
        {
            string envPrefix = ConfigurationManager.AppSettings.Get("ApplicationEnv");
            string appName = ConfigurationManager.AppSettings.Get("ApplicationName");

            RaxCachePrefix = String.Format("Curry_{0}_{1}", appName, envPrefix);
            ValidForTimeSpan = new TimeSpan(0, 0, 30);
            client = new MemcachedClient();
        }

        /// <summary>
        /// Gets the specified value based on Key and callback.
        /// Caution: I have not tested this extensively, use this at your own peril.
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="key">The key.</param>
        /// <param name="callback">The callback.</param>
        /// <returns></returns>
        public static T Get<T>(string key, Func<T> callback)
        {
            T item = client.Get<T>(RaxCachePrefix + key.Trim());
                if (item == null)
                {
                    item = callback();
                    Insert(key.Trim(), item);
                }
                return item;
        }

        /// <summary>
        /// Gets the specified value from cache based on Key.
        /// </summary>
        /// <typeparam name="T"></typeparam>
        /// <param name="key">The key.</param>
        /// <returns></returns>
        public static T Get<T>(string key)
        {
            T item = client.Get<T>(RaxCachePrefix + key.Trim());            
                return item;
        }

        /// <summary>
        /// Gets the value as object based on key.
        /// </summary>
        /// <param name="key">The key.</param>
        /// <returns></returns>
        public static object Get(string key)
        {
            return client.Get(RaxCachePrefix + key.Trim());
        }

        /// <summary>
        /// Tries to get an object from cache. Returns true if found.
        /// </summary>
        /// <param name="key">The key.</param>
        /// <param name="value">The value.</param>
        /// <returns></returns>
        public static bool TryGet(string key, out object value)
        {
            return client.TryGet(RaxCachePrefix + key.Trim(), out value);
        }

        /// <summary>
        /// Inserts object into cache.
        /// </summary>
        /// <param name="key">The key.</param>
        /// <param name="value">The value.</param>
        /// <returns></returns>
        public static bool Insert(string key, object value)
        {
            return client.Store(StoreMode.Set, RaxCachePrefix + key.Trim(), value, ValidForTimeSpan);        
        }

        /// <summary>
        /// Removes the object from cache 
        /// </summary>
        /// <param name="key">The key.</param>
        /// <returns></returns>
        public static bool Remove(string key)
        {
            return client.Remove(RaxCachePrefix + key.Trim());
        }

        /// <summary>
        /// Inserts object into cache for a specific timespan
        /// </summary>
        /// <param name="key">The key.</param>
        /// <param name="value">The value.</param>
        /// <param name="validFor"> valid for.</param>
        /// <returns></returns>
        public static bool Insert(string key, object value, TimeSpan validFor)
        {
            bool success = client.Store(StoreMode.Set, RaxCachePrefix + key.Trim(), value, validFor);

            if (!success)
            {  }

            return success;
        }

      

    }
}

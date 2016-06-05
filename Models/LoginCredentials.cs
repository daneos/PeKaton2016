using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class LoginCredentials
    {
        public string UserEmail { get; set; }
        public string HashedPassword { get; set; }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class Group
    {
        public int GroupId { get; set; }
        public virtual List<Employee> Members { get; set; }
        public string GroupName { get; set; }
    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class Event
    {
        public int EventId { get; set; }
        public string EventName { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public virtual Room PlaceInt { get; set; }
        public string PlaceExt { get; set; }
        public string Note { get; set; }
        public virtual List<Employee> Memebers { get; set; }
        public bool Private { get; set; }
        public virtual Employee Owner { get; set; }
        public int Done { get; set; }
        public bool Finished { get; set; }


    }
}
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class RoomTimeSpan
    {
        public string RoomId { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime EndTime { get; set; }
        public string StartTimeS { get; set; }
        public string EndTimeS { get; set; }
        public virtual Employee Owner { get; set; }
    }
}
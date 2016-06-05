using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace Pekaton2016.Models
{
    public class Voucher
    {
        public string Description { get; set; }
        public string Name { get; set; }
        public int VoucherId { get; set; }
        public string Thumb { get; set; }
        public string Code { get; set; }
    }
}
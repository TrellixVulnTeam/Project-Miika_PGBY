using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AkiraBot
{
    public partial class Form5 : Form
    {
        public Form5()
        {
            InitializeComponent();
        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {
            Form6 frm6 = new Form6();
            this.Hide();
            frm6.Show();
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {
            Form4 frm4 = new Form4();
            this.Hide();
            frm4.Show();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            Form3 frm3 = new Form3();
            this.Hide();
            frm3.Show();
        }
    }
}

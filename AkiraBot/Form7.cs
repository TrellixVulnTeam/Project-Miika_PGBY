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
    public partial class Form7 : Form
    {
        public Form7()
        {
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form1 frm1 = new Form1();
            this.Hide();
            frm1.Show();
        }

        private void textBox1_Validating(object sender, CancelEventArgs e)
        {
           // if (string.IsNullOrWhiteSpace(textBox1.Text))
            //{
             //   e.Cancel = true;
              //  textBox1.Focus();
              //  textBox1.SetError(textBox1, "Name should not be left blank!");
          //  }
           // else
           // {
            //    e.Cancel = false;
              //  errorProviderApp.SetError(textBoxName, "");
            //}
        }
    }
}

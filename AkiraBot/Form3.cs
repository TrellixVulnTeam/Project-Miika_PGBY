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
    public partial class Form3 : Form
    {
        public Form3()
        {
            InitializeComponent();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            Form1 form = new Form1();
            form.Show();
            this.Hide();
        }

        private void button1_Click(object sender, EventArgs e)
        {
            if (textBox1.Text == "lojitha" && textBox2.Text == "lojitha123")
            {
              
                Form5 frm5 = new Form5();
                this.Hide();
                frm5.Show();
            }
            else
            {
                MessageBox.Show("Incorrect username and password", "Stop", MessageBoxButtons.OK, MessageBoxIcon.Error);
            
            }

        }
    }
}

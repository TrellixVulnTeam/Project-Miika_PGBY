using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace AkiraBot
{
    public partial class Form4 : Form
    {
        public Form4()
        {
            InitializeComponent();
        }

        class round : TextBox
        {
            [System.Runtime.InteropServices.DllImport("gdi32.dll", EntryPoint = "CreateRoundRectRgn")]
            private static extern IntPtr CreateRoundRectRgn
            (
                int nLeftRect, // X-coordinate of upper-left corner or padding at start
                int nTopRect,// Y-coordinate of upper-left corner or padding at the top of the textbox
                int nRightRect, // X-coordinate of lower-right corner or Width of the object
                int nBottomRect,// Y-coordinate of lower-right corner or Height of the object
                                //RADIUS, how round do you want it to be?
                int nheightRect, //height of ellipse 
                int nweightRect //width of ellipse
            );
            protected override void OnCreateControl()
            {
                base.OnCreateControl();
                this.Region = System.Drawing.Region.FromHrgn(CreateRoundRectRgn(2, 3, this.Width, this.Height, 15, 15)); //play with these values till you are happy
            }
        }

        private void pictureBox2_Click(object sender, EventArgs e)
        {

        }

        private void pictureBox3_Click(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
        {
            Form5 frm5 = new Form5();
            this.Hide();
            frm5.Show();
        }

        private void label3_Click(object sender, EventArgs e)
        {
            Form5 frm5 = new Form5();
            this.Hide();
            frm5.Show();
        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void pictureBox1_Click(object sender, EventArgs e)
        {

        }

        private void Form4_Load(object sender, EventArgs e)
        {

        }
    }
}

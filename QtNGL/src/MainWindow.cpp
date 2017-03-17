#include "MainWindow.h"
#include "ui_MainWindow.h"


MainWindow::MainWindow(QWidget *parent) :QMainWindow(parent), m_ui(new Ui::MainWindow)
{
  m_ui->setupUi(this);

  m_gl=new  NGLScene(this, 3);

  m_ui->s_mainWindowGridLayout->addWidget(m_gl,0,0,2,1);
  connect(m_ui->m_changeC,SIGNAL(clicked()),m_gl,SLOT(setColour()));



  connect(m_ui->m_addBoid,SIGNAL(clicked()),m_gl,SLOT(addBoid()));
  connect(m_ui->m_removeBoid,SIGNAL(clicked()),m_gl,SLOT(removeBoid()));
}

MainWindow::~MainWindow()
{
    delete m_ui;
}

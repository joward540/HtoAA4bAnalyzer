//
// This macro is use to convert nanoAOD(plus) ntuple to histograms
// Usage: root -l -b -q HtoaaAna.cxx++

#include <iostream>
#include <iomanip>
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TPad.h"
#include "stdlib.h" 
#include "TStyle.h"
#include "TGraph.h"
#include "TAxis.h"
#include "TLegend.h"
#include "TFile.h"
#include "string.h"
#include "TChain.h"
#include "TTree.h"
#include "TROOT.h"
#include "TGaxis.h"
#include "TLatex.h"
#include "TBufferFile.h"
#include "TLorentzVector.h"
#include "TPaveStats.h"
#include <fstream>
#include <string>
#include <vector> // or <list>

void HtoaaAna() {
  
  TH1::SetDefaultSumw2(true);

  gROOT->Reset();
  gStyle->SetOptStat("nemruo");

  // Chain your tree
  TChain *t1 = new TChain("Events");
  
  string inDir = "/cms/data/store/mc/RunIII2024Summer24NanoAODv15/GluGluH-01J-HToAATo4B_Par-M-35_TuneCP5_13p6TeV_madgraph-pythia8/NANOAODSIM/150X_mcRun3_2024_realistic_v2-v2/2520000/";

  // Add a single file
  //string infile = "0afb91ad-bf79-4830-ba1a-ebb5b2a0b4b4.root";  
  //t1->Add((inDir + infile).c_str());

  // Add multiple files
  std::vector<std::string> words;
  std::ifstream file("List_GluGluH-01J-HToAATo4B_Par-M-35.txt");
  std::string word;
  // Read words one by one using the extraction operator (>>) until the end of the file
  while (file >> word) {
    words.push_back(word); // Add the read word to the vector
  }
  for (const std::string& w : words) {
    t1->Add((inDir + w).c_str());
    std::cout << w << std::endl;
  }
  
  // MuMonitor validation example with Muon 2010 dataset
  //string outfile = "HtoaaAna_AK8_Histos.root";              // version NanoAODRun1_v1
  string outfile = "HtoaaAna_RECO_Histos.root";          

  TFile fout((outfile).c_str(),"RECREATE");

  cout << "writing to " << outfile << endl;

////////////////////////////////////////////////////////////////////////////////
///////////////////////// Declare input variables start ////////////////////////
////////////////////////////////////////////////////////////////////////////////
  
  // Variables in the tree
  UInt_t run;
  ULong64_t event;  // use this for newer versions starting from .zerobias
  UInt_t luminosityBlock;
  UInt_t nLHEPart;
  UInt_t nGenPart;

  // should replace 128 by parameter; check whether value is appropriate!
  Float_t LHEPart_eta[128];
  Float_t LHEPart_mass[128];
  Int_t   LHEPart_pdgId[128];
  Float_t LHEPart_phi[128];
  Float_t LHEPart_pt[128];
  Int_t LHEPart_status[128];

  // should replace 128 by parameter; check whether value is appropriate!
  Float_t GenPart_eta[5000];
  Float_t GenPart_mass[5000];
  Int_t   GenPart_pdgId[5000];
  Float_t GenPart_phi[5000];
  Float_t GenPart_pt[5000];
  Int_t GenPart_status[5000];
  Int_t GenPart_statusFlags[5000];

  // Variables defined in this code
  TLorentzVector p4b;
  TLorentzVector p4btot;
  
////////////////////////////////////////////////////////////////////////////////
/////////////////////////// Declare input variables end ////////////////////////
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
/////////////////////////// Activate branches start ////////////////////////////
////////////////////////////////////////////////////////////////////////////////

  // Disable all branches
  t1->SetBranchStatus("*", 0);

  // Read only selected branches
  t1->SetBranchStatus("run", 1);
  t1->SetBranchStatus("event", 1);
  t1->SetBranchStatus("luminosityBlock", 1);
  t1->SetBranchStatus("nGenPart", 1);
  t1->SetBranchStatus("GenPart_eta", 1);
  t1->SetBranchStatus("GenPart_mass", 1);
  t1->SetBranchStatus("GenPart_pdgId", 1);
  t1->SetBranchStatus("GenPart_phi", 1);
  t1->SetBranchStatus("GenPart_pt", 1);
  t1->SetBranchStatus("GenPart_status", 1);
  t1->SetBranchStatus("GenPart_statusFlags", 1);

////////////////////////////////////////////////////////////////////////////////
///////////////////////////// Activate branches end ////////////////////////////
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
////////////////////// Get the address of the branch start /////////////////////
////////////////////////////////////////////////////////////////////////////////

  t1->SetBranchAddress("run", &run);
  t1->SetBranchAddress("event", &event);
  t1->SetBranchAddress("luminosityBlock", &luminosityBlock);  
  t1->SetBranchAddress("nGenPart", &nGenPart);
  t1->SetBranchAddress("GenPart_eta", GenPart_eta);
  t1->SetBranchAddress("GenPart_mass", GenPart_mass);
  t1->SetBranchAddress("GenPart_pt", GenPart_pt);
  t1->SetBranchAddress("GenPart_phi", GenPart_phi);
  t1->SetBranchAddress("GenPart_pdgId", GenPart_pdgId);
  t1->SetBranchAddress("GenPart_status", GenPart_status);
  t1->SetBranchAddress("GenPart_statusFlags", GenPart_statusFlags);

////////////////////////////////////////////////////////////////////////////////
/////////////////////// Get the address of the branch end //////////////////////
////////////////////////////////////////////////////////////////////////////////

////////////////////////////////////////////////////////////////////////////////
///////////////////////// Declare your histogram start /////////////////////////
////////////////////////////////////////////////////////////////////////////////
  
  // run nr, event nr, and lumi section for all events that have been analyzed
  TH1D *GM_run = new TH1D("Run number", "Run number", 3100, 146400, 149500);
  TH1D *GM_event = new TH1D("Event number", "Event number", 2000, 0, 2000000000);
  TH1D *GM_luminosityBlock = new TH1D("Lumi section", "Lumi section", 300, 0, 3000);

  
  //
  TH1D *h_HiggsPt_Gen_First = new TH1D("h_HiggsPt_Gen_First", "h_HiggsPt_Gen_First", 50, 0., 500.);
  TH1D *h_HiggsPt_Greaterthan1_Gen_First = new TH1D("h_HiggsPt_Greaterthan1_Gen_First", "h_HiggsPt_Greaterthan1_Gen_First", 50, 0., 500.);
  TH1D *h_HiggsPt_Gen_Last = new TH1D("h_HiggsPt_Gen_Last", "h_HiggsPt_Gen_Last", 50, 0., 500.);
  TH1D *h_HiggsPhi_Gen_First = new TH1D("h_HiggsPhi_Gen_First", "h_HiggsPhi_Gen_First", 50, -3.2, 3.2);
  TH1D *h_HiggsPhi_Gen_First_Pt_GreaterThan1 = new TH1D("h_HiggsPhi_Gen_First_Pt_GreaterThan1", "h_HiggsPhi_Gen_First_Pt_GreaterThan1", 50, -3.2, 3.2); 
  TH1D *h_HiggsPhi_Gen_Last = new TH1D("h_HiggsPhi_Gen_Last", "h_HiggsPhi_Gen_Last", 50, -3.2, 3.2);
  TH1D *h_HiggsEta_Gen_First = new TH1D("h_HiggsEta_Gen_First", "h_HiggsEta_Gen_First", 50, -7., 7.);
  TH1D *h_HiggsEta_Gen_Last = new TH1D("h_HiggsEta_Gen_Last", "h_HiggsEta_Gen_Last", 50, -7., 7.);
  TH1D *h_HiggsMass_Gen_First = new TH1D("h_HiggsMass_Gen_First", "h_HiggsMass_Gen_First", 50, 124., 126.);
  TH1D *h_HiggsMass_Gen_Last = new TH1D("h_HiggsMass_Gen_Last", "h_HiggsMass_Gen_Last", 50, 124., 126.);
  TH2D *h2_HiggsPt_GenFirst_GenLast = new TH2D("h2_HiggsPt_GenFirst_GenLast", "h2_HiggsPt_GenFirst_GenLast", 100, 0., 1000., 100, 0., 1000.);
  TH2D *h2_HiggsPt_Cut_GenFirst_GenLast = new TH2D("h2_HiggsPt_Cut_GenFirst_GenLast", "h2_HiggsPt_Cut_GenFirst_GenLast", 100, 0., 1000., 100, 0., 1000.);
////////////////////////////////////////////////////////////////////////////////
////////////////////////// Declare your histogram end //////////////////////////
////////////////////////////////////////////////////////////////////////////////
  
  Int_t nevent = t1->GetEntries();
  cout << "entries = " << nevent << endl;

////////////////////////////////////////////////////////////////////////////////
////////////////////////////// Start analyze! //////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
  
  // Loop over all events
  for (int aa = 0; aa < nevent; aa++) {
 
    if (aa>100000) continue; /// still not too many events yet
    if (aa % 100 == 0) cout << "event nr " << aa << endl;
    
    // Get the entry of your event
    t1->GetEntry(aa);

    // fill histograms
    GM_run->Fill(run);
    GM_event->Fill(event);
    GM_luminosityBlock->Fill(luminosityBlock);

    // GenPart analysis
    //
    int isFirst=0;
    int isLast=0;
    // Loop over gen particles
    for (unsigned int bb = 0; bb < nGenPart; bb++) {
      
      if (abs(GenPart_pdgId[bb])==25){
	/*
	  std::cout << GenPart_pt[bb] << " " 
	  << GenPart_eta[bb] << " " 
	  << GenPart_phi[bb] << " " 
	  << GenPart_status[bb] << " " 
	  << GenPart_statusFlags[bb] << " " 
	  << GenPart_pdgId[bb] << std::endl;
	*/
	if (GenPart_status[bb]==22) isFirst=bb;
	if (GenPart_status[bb]==62) isLast=bb;
	//std::cout << (GenPart_statusFlags[bb] & 1) << std::endl;
	//std::cout << (GenPart_statusFlags[bb] & (1U << 12)) << std::endl;      
	//std::cout << (GenPart_statusFlags[bb] & (1U << 13)) << std::endl;      
      }

      // https://cmssdt.cern.ch/lxr/source/DataFormats/HepMCCandidate/interface/GenStatusFlags.h?v=CMSSW_16_0_X_2025-12-02-2300#0030
      // if ((GenPart_statusFlags[bb] & (1U << 12)) >0 && abs(GenPart_pdgId[bb])==25){
      // 	if (isFirst>0) std::cout << "Warning: Another kIsFirstCopy Higgs??? " << bb <<std::endl;
      // 	isFirst=bb;
      // }
      // if ((GenPart_statusFlags[bb] & (1U << 13)) > 0 && abs(GenPart_pdgId[bb])==25){
      // 	if (isLast) std::cout << "Warning: Another kIsLastCopy Higgs??? " << bb << std::endl;
      // 	isLast=bb;
      // }

    }

    //std::cout << "event # etc: " << event << " " << isFirst << " " << isLast << std::endl;
    
    h_HiggsPt_Gen_First->Fill(GenPart_pt[isFirst]); 
    
    if (GenPart_pt[isFirst] > 1.0) {
	    h_HiggsPt_Greaterthan1_Gen_First->Fill(GenPart_pt[isFirst]);
    }
    
    h_HiggsPt_Gen_Last->Fill(GenPart_pt[isLast]);
    h_HiggsPhi_Gen_First->Fill(GenPart_phi[isFirst]);
    
    if (GenPart_pt[isFirst] > 1.0) {
	    h_HiggsPhi_Gen_First_Pt_GreaterThan1->Fill(GenPart_phi[isFirst]);
    }
    
    h_HiggsPhi_Gen_Last->Fill(GenPart_phi[isLast]);
    h_HiggsEta_Gen_First->Fill(GenPart_eta[isFirst]);
    h_HiggsEta_Gen_Last->Fill(GenPart_eta[isLast]);
    h_HiggsMass_Gen_First->Fill(GenPart_mass[isFirst]);
    h_HiggsMass_Gen_Last->Fill(GenPart_mass[isLast]);
    h2_HiggsPt_GenFirst_GenLast->Fill(GenPart_pt[isFirst], GenPart_pt[isLast]);

    if (GenPart_pt[isFirst] > 1.0) {
	    h2_HiggsPt_Cut_GenFirst_GenLast->Fill(GenPart_pt[isFirst], GenPart_pt[isLast]);
    }
  }
////////////////////////////////////////////////////////////////////////////////
/////////////////////////////// End analyze! ///////////////////////////////////
////////////////////////////////////////////////////////////////////////////////
  
////////////////////////////////////////////////////////////////////////////////
//////////////////////// write histograms and close file ///////////////////////
////////////////////////////////////////////////////////////////////////////////
  
  // Write out the histograms
  GM_run->Write();
  GM_event->Write();
  GM_luminosityBlock->Write();
  h_HiggsPt_Gen_First->Write();
  h_HiggsPt_Greaterthan1_Gen_First->Write();
  h_HiggsPt_Gen_Last->Write();
  h_HiggsPhi_Gen_First->Write();
  h_HiggsPhi_Gen_First_Pt_GreaterThan1->Write();
  h_HiggsPhi_Gen_Last->Write();
  h_HiggsEta_Gen_First->Write();
  h_HiggsEta_Gen_Last->Write();
  h_HiggsMass_Gen_First->Write();
  h_HiggsMass_Gen_Last->Write();
  h2_HiggsPt_GenFirst_GenLast->Write();
  h2_HiggsPt_Cut_GenFirst_GenLast->Write(); 
  fout.Close();

  gROOT->ProcessLine(".q");

  } // end of script


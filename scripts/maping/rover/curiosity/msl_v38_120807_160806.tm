KPL/MK

   This meta-kernel lists a subset of kernels from the meta-kernel
   msl_v38.tm provided in the MSL-M-SPICE-6-V1.0 SPICE PDS3 archive,
   covering the whole or a part of the customer requested time period
   from 2012-08-07T00:00:00.000 to 2016-08-06T00:00:00.000.

   The documentation describing these kernels can be found in the
   complete MSL-M-SPICE-6-V1.0 SPICE PDS3 archive available at this URL

   https://naif.jpl.nasa.gov/pub/naif/pds/data/msl-m-spice-6-v1.0/mslsp_1000

   To use this meta-kernel users may need to modify the value of the
   PATH_VALUES keyword to point to the actual location of the archive's
   ``data'' directory on their system. Replacing ``/'' with ``\''
   and converting line terminators to the format native to the user's
   system may also be required if this meta-kernel is to be used on a
   non-UNIX workstation.

   This meta-kernel was created by the NAIF node's SPICE PDS archive
   subsetting service version 2.1 on Sun Apr  6 13:31:02 PDT 2025.

 
   \begindata
 
      PATH_VALUES     = (
                         './data'
                        )
 
      PATH_SYMBOLS    = (
                         'KERNELS'
                        )
 
      KERNELS_TO_LOAD = (
                         '$KERNELS/lsk/naif0012.tls'
                         '$KERNELS/pck/pck00008.tpc'
                         '$KERNELS/sclk/msl_lmst_ops120808_v1.tsc'
                         '$KERNELS/sclk/msl_76_sclkscet_refit_t2.tsc'
                         '$KERNELS/fk/msl_v08.tf'
                         '$KERNELS/ik/msl_aux_v00.ti'
                         '$KERNELS/ik/msl_chrmi_20120731_c03.ti'
                         '$KERNELS/ik/msl_hbla_20120731_c03.ti'
                         '$KERNELS/ik/msl_hblb_20120731_c03.ti'
                         '$KERNELS/ik/msl_hbra_20120731_c03.ti'
                         '$KERNELS/ik/msl_hbrb_20120731_c03.ti'
                         '$KERNELS/ik/msl_hfla_20120731_c03.ti'
                         '$KERNELS/ik/msl_hflb_20120731_c03.ti'
                         '$KERNELS/ik/msl_hfra_20120731_c03.ti'
                         '$KERNELS/ik/msl_hfrb_20120731_c03.ti'
                         '$KERNELS/ik/msl_mahli_20120731_c02.ti'
                         '$KERNELS/ik/msl_mardi_20120731_c02.ti'
                         '$KERNELS/ik/msl_ml_20120731_c03.ti'
                         '$KERNELS/ik/msl_mr_20120731_c03.ti'
                         '$KERNELS/ik/msl_nla_20120731_c04.ti'
                         '$KERNELS/ik/msl_nlb_20130530_c05.ti'
                         '$KERNELS/ik/msl_nra_20120731_c04.ti'
                         '$KERNELS/ik/msl_nrb_20130530_c05.ti'
                         '$KERNELS/ik/msl_struct_v01.ti'
                         '$KERNELS/spk/msl_struct_v02.bsp'
                         '$KERNELS/spk/de425s.bsp'
                         '$KERNELS/spk/mar085s.bsp'
                         '$KERNELS/spk/msl_ls_ops120808_iau2000_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_0000_2003_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2003_2127_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2127_2224_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2224_2358_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2358_2482_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2482_2579_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2579_2713_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2713_2837_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2837_2934_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_2934_3068_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3068_3192_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3192_3289_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3289_3423_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3423_3547_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3547_3644_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3644_3778_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3778_3902_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3902_3999_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_3999_4133_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_4133_4257_v1.bsp'
                         '$KERNELS/spk/msl_surf_rover_loc_4257_4354_v1.bsp'
                         '$KERNELS/ck/msl_ra_toolsref_v1.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0000_0089_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0000_0089_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0000_0089_v2.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0000_0089_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0000_0089_v2.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0000_0089_v2.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0089_0179_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0089_0179_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0089_0179_v2.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0089_0179_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0089_0179_v2.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0089_0179_v2.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0179_0269_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0179_0269_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0179_0269_v2.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0179_0269_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0179_0269_v2.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0179_0269_v2.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0269_0359_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0269_0359_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0269_0359_v2.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0269_0359_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0269_0359_v2.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0269_0359_v2.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0359_0449_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0359_0449_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0359_0449_v2.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0359_0449_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0359_0449_v2.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0359_0449_v2.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0449_0583_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0449_0583_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0449_0583_v2.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0449_0583_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0449_0583_v2.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0449_0583_v2.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0583_0707_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0583_0707_v2.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0583_0707_v2.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0583_0707_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0583_0707_v2.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0583_0707_v2.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0707_0804_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0707_0804_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0707_0804_v1.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0707_0804_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0707_0804_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0707_0804_v1.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0804_0938_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0804_0938_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0804_0938_v1.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0804_0938_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0804_0938_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0804_0938_v1.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_0938_1062_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_0938_1062_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_0938_1062_v1.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_0938_1062_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_0938_1062_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_0938_1062_v1.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_1062_1159_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_1062_1159_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_1062_1159_v1.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_1062_1159_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_1062_1159_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_1062_1159_v1.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_1159_1293_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_1159_1293_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_1159_1293_v1.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_1159_1293_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_1159_1293_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_1159_1293_v1.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_1293_1417_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_1293_1417_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_1293_1417_v1.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_1293_1417_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_1293_1417_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_1293_1417_v1.bc'
                         '$KERNELS/ck/msl_surf_hga_tlm_1417_1514_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmenc_1417_1514_v1.bc'
                         '$KERNELS/ck/msl_surf_ra_tlmres_1417_1514_v1.bc'
                         '$KERNELS/ck/msl_surf_rover_tlm_1417_1514_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmenc_1417_1514_v1.bc'
                         '$KERNELS/ck/msl_surf_rsm_tlmres_1417_1514_v1.bc'
                        )
 
   \begintext
 


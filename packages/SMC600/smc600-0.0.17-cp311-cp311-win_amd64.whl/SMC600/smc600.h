#include <iostream>
#include <string>
#include <vector>

using namespace std;

#include "LTSMC.h"

static short board_init_e(unsigned short CardNo, unsigned short type, char *pconnectstring, unsigned long dwBaudRate) {
    return smc_board_init(CardNo, type, pconnectstring, dwBaudRate);
}

static short board_reset_e(unsigned short CardNo) {
    return smc_board_reset(CardNo);
}

static short board_close_e(unsigned short CardNo) {
    return smc_board_close(CardNo);
}

static short get_card_version_list(unsigned short CardNo, unsigned long *card_version_list) {
    return smc_get_card_version(CardNo, card_version_list);
}

static short get_equiv(unsigned short CardNo, unsigned short axis, double *equiv) {
    return smc_get_equiv(CardNo, axis, equiv);
}

static short set_equiv_e(unsigned short CardNo, unsigned short axis, double equiv) {
    return smc_set_equiv(CardNo, axis, equiv);
}

static short set_alm_mode_e(unsigned short CardNo, unsigned short axis, unsigned short enable, unsigned short alm_logic,
                            unsigned short alm_action) {
    return smc_set_alm_mode(CardNo, axis, enable, alm_logic, alm_action);
}

static short write_sevon_pin_e(unsigned short CardNo, unsigned short axis, unsigned short on_off) {
    return smc_write_sevon_pin(CardNo, axis, on_off);
}

static short set_pulse_outmode_e(unsigned short CardNo, unsigned short axis, unsigned short outmode) {
    return smc_set_pulse_outmode(CardNo, axis, outmode);
}

static short
set_profile_e(unsigned short CardNo, unsigned short axis, double Min_Vel, double Max_Vel, double Tacc, double Tdec,
              double Stop_Vel) {
    return smc_set_profile_unit(CardNo, axis, Min_Vel, Max_Vel, Tacc, Tdec, Stop_Vel);
}

static short set_s_profile_e(unsigned short CardNo, unsigned short axis, unsigned short s_mode, double s_para) {
    return smc_set_s_profile(CardNo, axis, s_mode, s_para);
}

static short set_homemode_e(unsigned short CardNo, unsigned short axis, unsigned short home_dir, double vel_mode,
                            unsigned short mode, unsigned short EZ_count) {
    return smc_set_homemode(CardNo, axis, home_dir, vel_mode, mode, EZ_count);
}

static short set_home_profile_e(unsigned short CardNo, unsigned short axis, double Min_Vel, double Max_Vel,
                                double Tacc, double Tdec) {
    return smc_set_home_profile_unit(CardNo, axis, Min_Vel, Max_Vel, Tacc, Tdec);
}

static short set_home_position_e(unsigned short CardNo, unsigned short axis, unsigned short enable, double position) {
    return smc_set_home_position_unit(CardNo, axis, enable, position);
}

static short home_move_e(unsigned short CardNo, unsigned short axis) {
    return smc_home_move(CardNo, axis);
}

static short pmove_e(unsigned short CardNo, unsigned short axis, double Dist, unsigned short posi_mode) {
    return smc_pmove_unit(CardNo, axis, Dist, posi_mode);
}

static short check_done(unsigned short CardNo, unsigned short axis) {
    return smc_check_done(CardNo, axis);
}

static short get_position(unsigned short CardNo, unsigned short axis, double* pos) {
    return smc_get_position_unit(CardNo, axis, pos);
}

static short set_position_e(unsigned short CardNo, unsigned short axis, double current_position) {
    return smc_set_position_unit(CardNo, axis, current_position);
}

static short get_encoder_unit(unsigned short ConnectNo, unsigned short axis, double* pos) {
    return smc_get_encoder_unit(ConnectNo, axis, pos);
}

static short set_encoder_unit_e(unsigned short ConnectNo,unsigned short axis,double encoder_value) {
    return smc_set_encoder_unit(ConnectNo, axis, encoder_value);
}

static short get_counter_inmode(unsigned short ConnectNo, unsigned short axis, unsigned short *mode) {
    return smc_get_counter_inmode(ConnectNo, axis, mode);
}

static short set_counter_inmode_e(unsigned short ConnectNo, unsigned short axis, unsigned short mode) {
    return smc_set_counter_inmode(ConnectNo, axis, mode);
}

static short get_backlash_unit(unsigned short ConnectNo, unsigned short axis, double *backlash) {
    return smc_get_backlash_unit(ConnectNo, axis, backlash);
}

static short set_backlash_unit_e(unsigned short ConnectNo, unsigned short axis, double backlash) {
    return smc_set_backlash_unit(ConnectNo, axis, backlash);
}

static short stop_e(unsigned short CardNo, unsigned short axis, unsigned short stop_mode) {
    return smc_stop(CardNo, axis, stop_mode);
}

static short emg_stop_e(unsigned short CardNo) {
    return smc_emg_stop(CardNo);
}

static short update_target_position_e(unsigned short CardNo, unsigned short axis, double dst) {
    return smc_update_target_position_unit(CardNo, axis, dst);
}

static short reset_target_position_e(unsigned short CardNo, unsigned short axis, double dist) {
    return smc_reset_target_position_unit(CardNo, axis, dist);
}

static short read_org_pin(unsigned short CardNo, unsigned short axis) {
    return smc_read_org_pin(CardNo, axis);
}

static short read_elp_pin(unsigned short CardNo, unsigned short axis) {
    return smc_read_elp_pin(CardNo, axis);
}

static short read_eln_pin(unsigned short CardNo, unsigned short axis) {
    return smc_read_eln_pin(CardNo, axis);
}

static unsigned long axis_io_status(unsigned short CardNo, unsigned short axis) {
    return smc_axis_io_status(CardNo, axis);
}


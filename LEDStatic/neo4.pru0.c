// Use rpmsg to control the NeoPixels via /dev/rpmsg_pru30
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>			// atoi
#include <string.h>
#include <pru_cfg.h>
#include <pru_intc.h>
#include <rsc_types.h>
#include <pru_rpmsg.h>
#include "resource_table_0.h"
#include "prugpio.h"

volatile register uint32_t __R30;
volatile register uint32_t __R31;

/* Host-0 Interrupt sets bit 30 in register R31 */
#define HOST_INT			((uint32_t) 1 << 30)	

/* The PRU-ICSS system events used for RPMsg are defined in the Linux device tree
 * PRU0 uses system event 16 (To ARM) and 17 (From ARM)
 * PRU1 uses system event 18 (To ARM) and 19 (From ARM)
 */
#define TO_ARM_HOST			16	
#define FROM_ARM_HOST		17

/*
* Using the name 'rpmsg-pru' will probe the rpmsg_pru driver found
* at linux-x.y.z/drivers/rpmsg/rpmsg_pru.c
*/
#define CHAN_NAME			"rpmsg-pru"
#define CHAN_DESC			"Channel 30"
#define CHAN_PORT			30

/*
 * Used to make sure the Linux drivers are ready for RPMsg communication
 * Found at linux-x.y.z/include/uapi/linux/virtio_config.h
 */
#define VIRTIO_CONFIG_S_DRIVER_OK	4

char payload[RPMSG_BUF_SIZE];

#define STR_LEN 32
#define LEN 64
#define	oneCyclesOn		700/5	// Stay on for 700ns
#define oneCyclesOff	600/5
#define zeroCyclesOn	350/5
#define zeroCyclesOff	800/5
#define resetCycles		51000/5	// Must be at least 50u, use 51u
#define out P9_29				// Bit number to output on

#define SPEED 20000000/5		// Time to wait between updates

uint32_t color[STR_LEN];	// green, red, blue

/*
 * main.c
 */
void main(void)
{
	struct pru_rpmsg_transport transport;
	uint16_t src, dst, len;
	volatile uint8_t *status;

	uint8_t r, g, b, w;
	int i, j;
	// Set everything to background
	for(i=0; i<STR_LEN; i++) {
		color[i] = 0x01000000;
	}

	/* Allow OCP master port access by the PRU so the PRU can read external memories */
	CT_CFG.SYSCFG_bit.STANDBY_INIT = 0;

	/* Clear the status of the PRU-ICSS system event that the ARM will use to 'kick' us */
#ifdef CHIP_IS_am57xx
	CT_INTC.SICR_bit.STATUS_CLR_INDEX = FROM_ARM_HOST;
#else
	CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;
#endif

	/* Make sure the Linux drivers are ready for RPMsg communication */
	status = &resourceTable.rpmsg_vdev.status;
	while (!(*status & VIRTIO_CONFIG_S_DRIVER_OK));

	/* Initialize the RPMsg transport structure */
	pru_rpmsg_init(&transport, &resourceTable.rpmsg_vring0, &resourceTable.rpmsg_vring1, TO_ARM_HOST, FROM_ARM_HOST);

	/* Create the RPMsg channel between the PRU and ARM user space using the transport structure. */
	while (pru_rpmsg_channel(RPMSG_NS_CREATE, &transport, CHAN_NAME, CHAN_DESC, CHAN_PORT) != PRU_RPMSG_SUCCESS);
	while (1) {
		/* Check bit 30 of register R31 to see if the ARM has kicked us */
		if (__R31 & HOST_INT) {
			/* Clear the event status */
#ifdef CHIP_IS_am57xx
			CT_INTC.SICR_bit.STATUS_CLR_INDEX = FROM_ARM_HOST;
#else
			CT_INTC.SICR_bit.STS_CLR_IDX = FROM_ARM_HOST;
#endif
			/* Receive all available messages, multiple messages can be sent per kick */
			while (pru_rpmsg_receive(&transport, &src, &dst, payload, &len) == PRU_RPMSG_SUCCESS) {
			    char *ret;	// rest of payload after front character is removed
			    int index;	// index of LED to control
			    // Input format is:  index red green blue
			    index = atoi(payload);	
			    // Update the array, but don't write it out.
			    if((index >=0) & (index < STR_LEN)) {
			    	ret = strchr(payload, ' ');	// Skip over index
				    r = strtol(&ret[1], NULL, 0);
				    ret = strchr(&ret[1], ' ');	// Skip over r, etc.
				    g = strtol(&ret[1], NULL, 0);
				    ret = strchr(&ret[1], ' ');
				    b = strtol(&ret[1], NULL, 0);
				    ret = strchr(&ret[1], ' ');
				    w = strtol(&ret[1], NULL, 0);

				    color[index] = (g<<24)|(r<<16)|(b<<8)|w;	// String wants GRB
			    }
			    // When index is -1, send the array to the LED string
			    if(index == -1) {
				    // Output the string
					for(j=0; j<STR_LEN; j++) {
						// Cycle through each bit
						for(i=(LEN-1); i>=0; i--) {
							if(color[j] & (0x1<<i)) {
								__R30 |= out;		// Set the GPIO pin to 1
								__delay_cycles(oneCyclesOn-1);
								__R30 &= ~out;	// Clear the GPIO pin
								__delay_cycles(oneCyclesOff-14);
							} else {
								__R30 |= out;		// Set the GPIO pin to 1
								__delay_cycles(zeroCyclesOn-1);
								__R30 &= ~(out);	// Clear the GPIO pin
								__delay_cycles(zeroCyclesOff-14);
							}
						}
					}
					// Send Reset
					__R30 &= ~out;	// Clear the GPIO pin
					__delay_cycles(resetCycles);

					// Wait
					__delay_cycles(SPEED);
			    }

			}
		}
	}
}

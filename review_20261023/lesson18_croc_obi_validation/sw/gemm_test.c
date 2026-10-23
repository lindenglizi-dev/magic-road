#include <stdint.h>
#include "uart.h"
#include "print.h"
#include "config.h"
#define GEMM_BASE (0x20001000u)
#define MMIO32(o) (*(volatile uint32_t *)(uintptr_t)(GEMM_BASE+(o)))
// A=I; C must match B, including sign-extended signed byte lanes.
int main(void) {
    uart_init();
    const uint32_t a[4]={0x00000001u,0x00000100u,0x00010000u,0x01000000u};
    const uint32_t b[4]={0xFE030201u,0x08070605u,0x0C0B0A09u,0x100F0E0Du};
    uint32_t i,j;
    MMIO32(0x00)=2u;
    for(i=0;i<4;i++){ MMIO32(0x10+4*i)=a[i]; MMIO32(0x20+4*i)=b[i]; }
    MMIO32(0x00)=1u;
    for(i=0;i<1000000u;i++) if(MMIO32(0x04)&2u) break;
    if(i==1000000u) { printf("GEMM TIMEOUT\n");uart_write_flush();return 1; }
    for(i=0;i<4;i++) for(j=0;j<4;j++) {
        int32_t expected=(int8_t)(b[i]>>(8*j));
        int32_t got=(int32_t)MMIO32(0x40+4*(4*i+j));
        if(got!=expected){printf("GEMM FAIL r=%u c=%u\n",i,j);uart_write_flush();return 2;}
    }
    printf("GEMM PASS 4x4\n");
    uart_write_flush();
    return 0;
}

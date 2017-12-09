    .data
    .balign 4

pin1:   .int    11
pin2:   .int    31
pin3:   .int    26
pin4:   .int    27
pin5:   .int    28
pin6:   .int    29
delayMs:    .int    1500
delayLED:    .int    500
OUTPUT = 1

    .text
    .global main
    .extern wiringPiSetup
    .extern delay
    .extern digitalWrite
    .extern pinMode

main: PUSH {ip,lr}
    BL wiringPiSetup
    MOV R1, #-1
    CMP R0, R1
    BNE init
    B done

init:
    LDR R0, =pin1
    LDR R0, [R0]
    MOV R1, #OUTPUT
    BL pinMode

    LDR R0, =pin2
    LDR R0, [R0]
    MOV R1, #OUTPUT
    BL pinMode

    LDR R0, =pin3
    LDR R0, [R0]
    MOV R1, #OUTPUT
    BL pinMode

    LDR R0, =pin4
    LDR R0, [R0]
    MOV R1, #OUTPUT
    BL pinMode

    LDR R0, =pin5
    LDR R0, [R0]
    MOV R1, #OUTPUT
    BL pinMode

    LDR R0, =pin6
    LDR R0, [R0]
    MOV R1, #OUTPUT
    BL pinMode

    @digitalWrite ON
    LDR R0, =pin1
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =delayLED
    LDR R0, [R0]
    BL delay

    LDR R0, =pin2
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =delayLED
    LDR R0, [R0]
    BL delay

    LDR R0, =pin3
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =delayLED
    LDR R0, [R0]
    BL delay

    LDR R0, =pin4
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =delayLED
    LDR R0, [R0]
    BL delay

    LDR R0, =pin5
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =delayLED
    LDR R0, [R0]
    BL delay

    LDR R0, =pin6
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =delayLED
    LDR R0, [R0]
    BL delay

    @delay
    LDR R0, =delayMs
    LDR R0, [R0]
    BL delay

    @digitalWrite OFF
    LDR R0, =pin1
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin2
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin3
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin4
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin5
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin6
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    @delay
    LDR R0, =delayMs
    LDR R0, [R0]
    BL delay

    LDR R0, =pin1
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin2
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin3
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin4
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin5
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin6
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    @delay
    LDR R0, =delayMs
    LDR R0, [R0]
    BL delay

    LDR R0, =pin1
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin2
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin3
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin4
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin5
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin6
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    @delay
    LDR R0, =delayMs
    LDR R0, [R0]
    BL delay

    LDR R0, =pin1
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin2
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin3
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin4
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin5
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    LDR R0, =pin6
    LDR R0, [R0]
    MOV R1, #1
    BL digitalWrite

    @delay
    LDR R0, =delayMs
    LDR R0, [R0]
    BL delay

    LDR R0, =pin1
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin2
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin3
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin4
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin5
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    LDR R0, =pin6
    LDR R0, [R0]
    MOV R1, #0
    BL digitalWrite

    B done

done:
    POP {ip, pc}

# Leadshine HBS Series — Hardware Installation Manual (transcripción completa)

- PDF original: hbs_series_hardware_manual_leadshine.pdf
- Fuente: https://refit.com.ua/wp-content/uploads/2024/04/hbshm_hardware_manual_for_hbs_series.pdf
- Páginas: 22
- Método: extracción del texto nativo con pypdf 6.14.2, modo layout.
- Alcance: se conserva todo el texto recuperable, separado por página. Los diagramas y fotografías permanecen normativos en el PDF original.

## Página 1

```text
Hardware Installation Manual
HBS Series Hybrid Servo
HBS57
HBS86
HBS86H


                                                                                                                                          HMN_HBS_R20121128
                                                                                                                               http://www.Leadshine.com
```

## Página 2

```text
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             ii
Safety Items

                                                                                                       Read this manual carefully before trying to install the stepper drive into your
                                                                                                       system. The people who setup the stepper drive should have a better
                              Notice              !                                                    understanding on electronics and mechanics. Contact Leadshine technical guys
                                                                                                       when you have questions on this document.


                                                                                                       Make sure the power supply voltage dose not exceed the drive                                                                                                       ’s input range.
                          Caution              !                                                       Double check the connections and make sure the power lead polarity is correct.


                                                                                                       Do not set high current for small stepper motor. It is possible that the motor will be
                       Warning               !                                                         damaged.


                                                                                                       Disconnect the motor from the load if you are not sure the move direction. Adjust
                          Caution              !                                                       the axis in the center before trying to run the motor.


                                       !                                                               Never disconnect the motor lead when the power source is energized.
                       Warning


                                                                                                                                                                                                                                                                                                                                                                                                                                                                     HWMN-ISS57-R20120411
```

## Página 3

```text
                                                                                                                                                                                                                                                           iii

                                                                                                    Table of Contents

Introduction to HBS                             ...................................................................................................................................................1
Getting Start                     .................................................................................................................................................................1
          Connecting Power Supply                                              ...............................................................................................................................2
          Connecting Motor                              ...............................................................................................................................................2
          Connecting Encoder                                   ..........................................................................................................................................3
          Connecting Control Signal                                              ...............................................................................................................................4
          Connecting to PC Software                                                .............................................................................................................................5
HBS Drive Configuration                                          ..........................................................................................................................................6
          Configuring HBS Drive by DIP Switches                                                                      ......................................................................................................7
          Configuring HBS Drive in PC Software                                                                     ........................................................................................................8
          Calculating Rotation Speed and Angle                                                                    .........................................................................................................9
Rotating the HBS Motor by Motion Controller                                                                                 ....................................................................................................9
Rotating the HBS Motor in PC Software                                                                      .............................................................................................................10
Power Supply Selection                                        ..........................................................................................................................................10
          Regulated or Unregulated Power Supply                                                                        ...................................................................................................10
          Multiple Drives                        ...................................................................................................................................................11
          Selecting Supply Voltage                                           ................................................................................................................................11
          Recommended Supply Voltage                                                     .....................................................................................................................12
Control Signal Wiring                                    ..............................................................................................................................................12
          NPN (Sinking) Control Signal Wiring                                                               ...........................................................................................................12
          PNP (Sourcing) Control Signal Wiring                                                                  ........................................................................................................13
          Differential Control Signal Wiring                                                          ................................................................................................................13
          Output Signal Wiring                                   .......................................................................................................................................14
          Wiring Notes                    ......................................................................................................................................................14
Control Signal Setup Timing                                                 .................................................................................................................................15
Current Control Detail                                       .............................................................................................................................................15
Fine Tuning                  ................................................................................................................................................................16
Protection Functions                                 ...............................................................................................................................................16
          Over-current Protection                                        ..................................................................................................................................16
          Over-voltage Protection                                        ..................................................................................................................................16
          Position Following Error Protection                                                              ............................................................................................................17
Frequently Asked Questions                                               .................................................................................................................................17
          Problem Symptoms and Possible Causes                                                                          ................................................................................................17
Warranty             ......................................................................................................................................................................18
          Exclusions                ..........................................................................................................................................................18
          Obtaining Warranty Service                                               ...........................................................................................................................18
          Warranty Limitations                                 .......................................................................................................................................18
          Shipping Failed Product                                          .................................................................................................................................18
          Contact Us                ..........................................................................................................................................................19


                                                                                                                                                                                                       HWMN-ISS57-R20120411
```

## Página 4

```text
                                                                                                                                                                                                                                                                              Hybrid Servo Hardware Installation Manual

Introduction to HBS

The HBS (Hybrid Servo Series) series hybrid servos offer an alternative for applications requiring high
performance and high reliability when the servo was the only choice, while it remains cost-effective.
The system includes a hybrid servo motor combined with a fully digital, high performance easy servo
drive. The internal encoder is used to close the position, velocity and current loops in real time, just
like servo systems. It combines the best of servo and stepper motor technologies, and delivers unique
capabilities and enhancements over both, while at a fraction of the cost of a servo system.


                                                                                                                                                                                                                                                                                                                                 Hybrid Drive

                                          Command Position                                                                                                                                                                                                                     Comparator                                                                                                                                                                                                                                                                                                                      Hybrid Motor

                                                                                                                                                                                                                                                                               Comp                                                                                                                        Amplifier                                                                                                                                                                                              Stepper Motor

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             Encoder


                                                                                                                                                                                                                                                                                                                                            Measured Position


Getting Start

To get start you need one HBS drive, one hybrid motor (stepper drive with encoder) and one power
supply for a first time evaluation. A full installation should include an indexer such as pulse generator,
PLC or motion controller. A PC with at least one serial port or one PC with USB-RS232 converter, you
can rotate the motor in PC software. It is recommended to use an indexer instead of PC software to
verify the full function of the HBS drive and motor.


                                                                                                                                                                                                                                                                                                                                                                                                                              1                                                                                                                                                                                                                             HWMN                                                  -HBS                              -R20120                                                    411
```

## Página 5

```text
                                                                                                                                                                        Hybrid Servo Hardware Installation Manual

                                                                                                                                                                                                                                                                           RS232 Cable


                                                                                                                                                                                                                                                                           Or              USB-232 Converter


                                                                                                                                                                                                                                                                                           Motion Controller

                              Power Supply                                                                                                                                                                                                                                                 Encoder Cable


                                                                                                                                                                                                                                    Motor Power Cable


Connecting Power Supply

Power supply connection is the simplest thing through this manual because it has only tow wires:
positive wire and negative wire. However you should caution the incorrect connection polarity. The
HBS drive a 6-pin pluggable screw connector that is used for both power supply connection and
motor connection. Looking at the drive cover you should find the printed                                                                                                                        “+Vdc   ” and    “GND  ” symbol.
Connect the positive wire to                                              “+Vdc   ” terminal and connect the negative wire to                                                                      “GND  ” terminal. Note
that the power should be off when you make the above connection.

Note   :  Do not exceed the input voltage range of the HBS drive. Please consult Power Supply
Selection chapter for the recommended supply voltage                                                                                                  .


                                                                                                                 +Vdc                                                                                                                                       + (Positive)
                      High Voltage
                                                                                                                 GND                                                                                                                                       - (Negative)


Connecting Motor

The HBS motor has 4 wires: A+, A-, B+ and B-. Just connect them to the corresponding terminals of
the HBS drive. Refer to the HBS drive or the HBS motor datasheet for the detailed motor specification
and wiring diagram.


                                                                                                                                                                                                                       2                                                                                                                   HWMN                        -HBS             -R20120                        411
```

## Página 6

```text
                                                                                                                                                                                             Hybrid Servo Hardware Installation Manual

                                                                                                                                                                                                                                                                                                                                      573SXX                                -EC-XXXX

                                                                                                                                             U                                                                                   U
                                                                                                                                              V                                                                                   V
                                                                                                                                            W                                                                                   W
                                             HBS57


                                                                                                                                                                                                                                                                                                                                      57HSXX                                  -EC-XXXX
                                                                                                                                           A+                                                                                  A+
                                             HBS86                                                                                          A-                                                                                  A-
                                                                                                                                           B+                                                                                  B+
                                             HBS86H                                                                                          B-                                                                                 B-


                                                                                                                                                                                                                                                                                                                                      86HSXX                                  -EC-XXXX


Connecting Encoder

As the HBS drive works in close-loop mode, it must know the actual motor position. The encoder
mounted in the motor offers such information. Note that the HBS drive will not work without
encoder feedback.
For HBS86 or HBS86H, as the encoder output of the motor is a HDD15 (High Density D-Sub 15-pin
connector) but the drive                                          ’s encoder input is a screw terminal, you need one more
extension/conversion cable for the encoder signal connection between drive and motor. One end of
this extension/conversion cable is a HDD15 socket and the other end is 6 flying wires with the cable
shielding. For HBS57, the encoder output can be connected to HBS drive directly.
Please refer to the HBS motors datasheet for the HDD15 connector pin out the extension/conversion
cable wire color definition.


                                                                                                                                                                                                                                                               3                                                                                                                                        HWMN                             -HBS                 -R20120                              411
```

## Página 7

```text
                                                                                                                                               Hybrid Servo Hardware Installation Manual


                                                                                                                                                                                                                                 573SX                X-EC-XXXX


                                                                                                                                                                                                                                              1                                 5
                                                                       Feedback                                                         Encoder Signals                                                                                    6                                10
                                                                                                                                                                                                                                            11                         15
                             HBS57


                                                                                         EB+                                                                                                                                            Encoder Cable
                             HBS86                                                        EB-
                                                                                         EA+                                            Encoder Signals
                             HBS86H                                                       EA-
                                                                                         VCC
                                                                                      EGND                                                  Color                    Name
                                                                                                                                               Red             VCC
                                                                                                                                           White                       GND
                                                                                                                                           Yellow                         B+
                                                                                                                                           Green                           B-
                                                                                                                                             Black                        A+
                                                                                                                                              Blue                         A-


                                                                                                                                                                                                                                                          1                                 5
                                                                                                                                                                                                                                                       6                                10
                                                                                                                                                                                                                                                         11                         15

                                                                                                                                                                                                                                       57HSXX-EC-XXXX
                                                                                                                                                                                                                                       86HSXX-EC-XXXX

Connecting Control Signal

The HBS drive accepts Pulse/Direction or CW/CCW control signals from 5V to 24V. As the drive                                                                                                                                                         ’s
signal input is differential, it can also interface with PNP (Sourcing) or NPN (Sinking) type control
signal. If the controller                               ’s output circuit is PNP (Sourcing) type, the pulse, direction and enable signal
share the same             ground       terminal from the controller                                                 . And if the controller                              ’s output circuit is NPN
(Sinking) type, both the pulse, direction and enable signal are refer to the same                                                                                              positive terminal
(5V/24V)             from the controller.
For the enable signal, apply 0V between ENA+ and ENA- or leave them unconnected to enables the
drivel. If it is unnecessary to disable the drive, just leave it unconnected.


                                                                                                                                                                      4                                                                                        HWMN                  -HBS         -R20120                 411
```

## Página 8

```text
                                                                                                                                                                                                    Hybrid Servo Hardware Installation Manual


                     Connecting to Differential Control Signal                                                                                                                                                                                                                                       Connecting to NPN (sinking) Control Signal


                      Controller                                                                                                                                                                             Drive                                                                                           Controller                                                                                                                                                                   Drive

                                   PUL+                                                                                                PUL+                                                                                                                                                                        VCC                                                                                                  PUL+
                                    PUL-                                                                                                PUL-                                                                                                                                                                                                                                                                             PUL-
                                                                                                                                                                                                                                                                                                                   PUL                                                                                                    DIR+
                                     DIR+                                                                                                DIR+
                                                                                                                                         DIR-                                                                                                                                                                                                                                                                             DIR-
                                     DIR-                                                                                                                                                                                                                                                                         DIR
                                                                                                                                         ENA+                                                                                                                                                                                                                                                                             ENA+
                                     ENA+                                                                                                                                                                                                                                                                                                                                                                                 ENA-
                                     ENA-                                                                                                ENA-                                                                                                                                                          ENABLE


                        Connecting to PNP (sourcing) Control

                      Controller                                                                                                                                                                             Drive


                           PUL                                                                                                          PUL+

                                                    VCC                                        PUL-

                          DIR                                                                                                            DIR+

                                                                                                                                         DIR-
               ENABLE                                                                                                                    ENA+

                                                                                                                                         ENA-


Connecting to PC Software

There is a RS232 communication port in the HBS drive. It is used to communicate with the tuning
software in PC and configured the drive. You can even rotate the motor in the software if you don                                                                                                                                                                  ’t
have a motion controller.
To connect HBS drive to PC software, first download the software from our website:
http://www.leadshine.com                                                                                                                        . You may also get it from our CD however it is recommended to get it
from the website because it is always the latest one. Install this software in your PC and make it ready
for use later.

                                                                                                                                                                                                                                            RS232 Cable                                                                                                                                                                                                                ProTuner


                                                                                                                                                                                                                                            Or                  USB-232 Converter


The second thing is the RS232 communication cable. It should be shipped with the kit if you include it
in the order. It is still possible to make this cable by yourself. One end of this cable is a RJ-11 header
and the other end of cable is a 9 pin D-Sub female connector.

                                                                                                                                                                                                                                                                              5                                                                                                                                                HWMN                               -HBS                  -R20120                                411
```

## Página 9

```text
                                                                                                                                                              Hybrid Servo Hardware Installation Manual

The third thing is the serial port. If your PC does not have serial port, a USB-to-Serial converter is
needed. Thus you can use this converter to simulate the serial port from a USB port.
Connect the HBS drive to the PC                                               ’s serial port or the UBS-232 converter via the RS232 communication
cable.          The power should be turned off when you perform any connections!                                                                                                                                                                                    Turn on the power and
start the software in PC.
The software appears a                                             Connect to drive               window when you open it. The baud rate and device
address are fixed and you only need to select the com port as per the actual serial port or the
mapping port of a USB-232 converter. Check the                                                                                    Device Manager                   for the mapping port number of
the USB-232 converter.


HBS Drive Configuration

It is necessary to configure the HBS drive for different HBS motor before sending pulse to it. The drive
should be properly configured before power-up. Otherwise you may encounter the problems like
high motor heating, big motor noise or even motor stall due to weak torque. For a quick start of the
HBS servo, there are not much parameters need to be configured. The following table gives the most
significant parameters of the HBS drive.

           Most Significant Parameters of the HBS Drive
                                                                                                      HBS57                                  HBS86, HBS86H
           Micro Step Resolution (PPR)                                                                                     4000 (Software)                                             1600 (DIP Switch)
           Holding Current Percentage (%)                                                                                        60% (Software)                                              60% (Software)
           Close-loop Current Limit Percentage (%)                                                                                       100% (Software)                                              100% (Software)
           Current Loop Kp                                                                                              Auto Tuning At Power-up                                                   1500 (Software)
           Current Loop Ki                                                                                               Auto Tuning At Power-up                                                   200(Software)
           Applied Motor                                                                                                573S09-EC-XXXX                                                                                                                                                                    86HS80-EC-XXXX
                                                                                                                                                                                                      573S20-EC-XXXX                                                                                      86HS40-EC-XXXX
           Matching Supply Voltage                                                                                            24-36VDC                                            60-100VDC


                                                                                                                                                                                                   6                                                                                                        HWMN                      -HBS            -R20120                     411
```

## Página 10

```text
                                                                                                                                      Hybrid Servo Hardware Installation Manual

By default, the HBS86 and HBS86H are configured according to the 86HSXX-EC-XXXX on 60VDC. The
HBS57 is configured automatically at power-up according to the connected motor and supply voltage.
For other HBS motors, it is recommended to modify these settings to get the optimizing performance
as shown in the following tables.

        Recommended                        Holding / Close-loop Current                                                  Percentage
                                               573S09-EC                                              573S20-EC                             57HS10-EC                              57HS20-EC                             86HS40-EC                              86HS80-EC
        Holding
        Current (%)                                       60%                    60%                    40%                    60%                     60%                     60%
        Close-loop                                                      100%                    100%                    100%                    100%                    100%                     100%
        Current Limit (%)
        HBS Drive                                    HBS57                     HBS57                     HBS86                   HBS86                   HBS86                   HBS86


        Recommended                          Current Loop Kp / Ki                                   of Different Supply Voltage
        HBS Motor                                   HBS Drive                            24VDC                          36VDC                           48VDC                           60VDC
        57HS10-EC-XXXX                                HBS86                   1500 / 200                        1000 / 300                       800 / 250                                N/A
        57HS20-EC-XXXX                                HBS86                     3700 / 200                      2000 / 300                        1500 / 200                               N/A
        86HS40-EC-XXXX                             HBS86(H)                           N/A                    4400 / 200                      3000 / 200                        2300 / 200
        86HS80-EC-XXXX                             HBS86(H)                           N/A                    4400 / 200                      3000 / 200                        2300 / 200

There are possible two methods to configure the HBS drive as follows, depending on the specific
drive.

Configuring HBS Drive by DIP Switches

There are 6 bits DIP switches in the HBS86 and HBS86H drive. SW1 to SW4 are used to set the micro
step resolution and SW5 are used to set the direction polarity.

                          !                                    1)  The 2-bit DIP switch in the HBS57 drive is not used. Ignore it.

                       Notice                                  2)  The SW6 in HBS86 and HBS86H has no used.


                 6-bit DIP Switches in HBS86/HBS86H


                                                                                                                                                    7                                                                              HWMN               -HBS         -R20120              411
```

## Página 11

```text
                                                                                                                           Hybrid Servo Hardware Installation Manual


                       HBS86 and HBS86H Micro Step Resolution Setting
                       Steps/Revolution                                                      SW1                         SW2                         SW3                         SW4
                       Software Configured
                        (Default 200)                                                on                       on                       on                       on
                       800                                                      off                       on                       on                       on
                       1600 (Factory Setting)                                                              on                                     off                                    on                                     on
                       3200                                                    off                         off                         on                          on
                       6400                                                    on                          on                          off                         on
                       12800                                                           off                         on                          off                         on
                       25600                                                 on                          off                         off                         on
                       51200                                                 off                         off                         off                         on
                       1000                                                    on                          on                          on                          off
                       2000                                                    off                         on                          on                          off
                       4000                                                    on                          off                         on                          off
                       5000                                                    off                         off                         on                          off
                       8000                                                    on                          on                          off                         off
                       10000                                                           off                         on                          off                         off
                       20000                                                           on                          off                         off                         off
                       40000                                                           off                         off                         off                         off

Configuring HBS Drive in PC Software

Please consult the                                   Connecting to PC Software                          chapter for how to connect the HBS drive to PC.
Suppose the tuning software has been open, click the                                                                                               Drive->Parameters                     to open the                                 Tool->Drive
Parameters            window. Double click the                                                            Value    column to modify the parameter. Don                                                              ’t forget to click
Download to Drive                                 to store the change to drive                                         ’s NVM. Please consult the HBS Drive Configuration
chapter for the recommended settings of different HBS motor. Please refer to the software manual
for more information.


                                                                                                                               8                                                                    HWMN             -HBS      -R20120           411
```

## Página 12

```text
                                                                                                                                                                                                                                                                       Hybrid Servo Hardware Installation Manual


Calculating Rotation Speed and Angle

You may also want to calculate the motor rotation speed and rotation angle, before commanding any
motion. If the pulse frequency and counts are known, they can be calculated as follows:

                                  Rotation Speed (RPM) = 60 * Pulse (Step) Frequency / Micro Step Resolution
                                  Rotation Angle (                      °)    = 360 * Pulse (Step) Counts / Micro Step Resolution
Rotating the HBS Motor by Motion Controller

Now everything is ready. You can start the controller or pulse generator to rotate the motor. Actually,
any device which gives high-to-low or low-to-high level changes can be used to move the motor. If it
is your first time installation, it is recommended to disconnect the motor shaft from the load in case
of accident. You can start from low pulse frequency then going to high. One triggered edge of the
pulse makes the motor move one micro angle. There is no minimum speed limit for HBS servo
however the maximum running speed will be determined by the input voltage and current setting.


                                                                                                                                                                                                                                                                                                                                                                                                                9                                                                                                                                                                                                                       HWMN                                               -HBS                             -R20120                                                   411
```

## Página 13

```text
                                                                                                                                                                                                          Hybrid Servo Hardware Installation Manual
Rotating the HBS Motor in PC Software

Not everyone has a motion controller. Or you may not know what motion controller is and how to
buy one. But you should have a personal computer which has at least one serial port or USB port. You
can rotate the HBS motor in PC software! There is a simple emulating controller that is used for
self-test in the HBS drive. It is not a full functionality controller but it do eliminates the troubles to
setup a real motion controller when you want to test the HBS drives or verify the connection in case
of problem.                    However, the performance you see in this emulating controller PC software CAN NOT
represents the actual motion controller                                                                 .


Click      Drive Setting                   ->Current Loop / Motion Test                                            to open the test window. Then click the                                                                     Motion Test
tab to open the emulating controller. Edit the trapezoid velocity profile and click the                                                                                                                                                   Start   button to
issue the motion.
Power Supply Selection

To achieve good driving performances, it is important to select supply voltage and output current
properly. Generally speaking, supply voltage determines the high speed performance of the motor,
while output current determines the output torque of the driven motor (particularly at lower speed).
Higher supply voltage will allow higher motor speed to be achieved, at the price of more noise and
heating. If the motion speed requirement is low, it                                                                                    ’s better to use lower supply voltage to decrease
noise, heating and improve reliability.

Regulated or Unregulated Power Supply

Both regulated and unregulated power supplies can be used to supply the drive. If regulated power
supplies (such as most switching supplies.) are indeed used, it is important to have large current

                                                                                                                                                                                                                                                                                      10                                                                                                                                                         HWMN                                 -HBS                   -R20120                                  411
```

## Página 14

```text
                                                                                                                                                                               Hybrid Servo Hardware Installation Manual

output rating to avoid problems like current clamp, for example using 4A supply for 3A motor-drive
operation. On the other hand, if unregulated supply is used, one may use a power supply of lower
current rating than that of motor (typically 50%                 ～70% of motor current). The reason is that the drive
draws current from the power supply capacitor of the unregulated supply only during the ON
duration of the PWM cycle, but not during the OFF duration. Therefore, the average current
withdrawn from power supply is considerably less than motor current. For example, two 3A motors
can be well supplied by one power supply of 4A rating.

Multiple Drives

It is recommended to have multiple drives to share one power supply to reduce cost, if the supply
has enough capacity. To avoid cross interference, DO NOT daisy-chain the power supply input pins of
the drives. Instead, please connect them to power supply separately.

Selecting Supply Voltage

Higher supply voltage can increase motor torque at higher speeds, thus helpful for avoiding losing
steps. However, higher voltage may cause bigger motor vibration at lower speed, and it may also
cause over-voltage protection or even drive damage. Therefore, it is suggested to choose only
sufficiently high supply voltage for intended applications, and it is suggested to use power supplies
with theoretical output voltage of drive                                                           ’s minimum + 10% to drive                                      ’s maximum                – 10%, leaving room
for power fluctuation and back-EMF.


Select Power Supply Voltage


                                                                 Driver Upper Input limitDriver Upper Input limit


                                                                 Driver Upper Input limit              –10%Driver Upper Input limit              –10%                                                                                                                Maximum Safe RatingMaximum Safe Rating


                                                                                                                                          Safe RegionSafe Region                                                                                                            TorqueTorque                                                                   HeatingHeating
                                                                                                                                                                                                                                                                             SpeedSpeed                                                                  VibrationVibration


                                                                 Driver Lower Input limit                            + 10%Driver Lower Input limit                            + 10%                                                                                  Minimum Safe RatingMinimum Safe Rating


                                                                 Driver Lower Input limitDriver Lower Input limit

                                                                    Driver Input VoltageDriver Input Voltage                                                                                                                                                      Power Supply VoltagePower Supply Voltage


                                                                                                                                                                                                                                 11                                                                                                                            HWMN                          -HBS               -R20120                          411
```

## Página 15

```text
                                                                                                                                                        Hybrid Servo Hardware Installation Manual

Recommended Supply Voltage

Both Leadshine                     ’s regulated and unregulated power supply has been designed specially for motion
control.

                           Motor                               Drive               Voltage Range                                                                                               Typical Voltage                                                 Leadshine Power Supply
                           57HS09-EC-XXXX                                                        HBS57                           DC(20-50)V                           DC 24V                       RPS2410(-L)
                           57HS20-EC-XXXX                                                        HBS57                           DC(20-50)V                           DC 36V                       RPS369
                           57HS10-EC-XXXX                                                        HBS86                           DC(30-80)V                           DC 36V                       RPS369
                           57HS20-EC-XXXX                                                        HBS86                           DC(30-80)V                           DC 36V                       RPS369
                           86HS40-EC-XXXX                                                        HBS86                           DC(30-80)V                           DC 60V                       RPS608
                           86HS80-EC-XXXX                                                        HBS86                           DC(30-80)V                           DC 60V                       RPS608
Control Signal Wiring

The HBS drive accepts both differential and single-ended control signals (including open-collector and
PNP output).                       Make sure the output port of the controller can sink or source 10mA at the least.                                                                                                                                                            If
you encounter the problem that motor does not rotating or losing steps, check whether or not the
controller can maintain 5V/24V output at any current and pulse frequency.

If the cable length is greater than 50cm, it is recommended to use twisted shielded pair cable for
these signal. Do not put the control signal cable together with the cables which is used for high
power or high current equipment, in case of electronic interference coupled into the control signal.

NPN (Sinking) Control Signal Wiring

If the motion controller is not differential output type, NPN type is recommended as it can sink more
current than PNP type. In this wiring, Pulse, Direction and Enable signal share the same VCC (positive)
terminal.

                                                                                                        Controller                                                                                                                                    Drive
                                                                                                                                                                     5-24V
                                                                                                  VCC
                                                                                                                                                                    Pulses                                                        PUL+


                                                                                                                                                                                                                                   PUL-

                                                                                                                                                                                                                                  DIR+
                                                                                                                                                                   Direction
                                                                                                                                                                                                                                   DIR-
                                                                                                                                                                     Enable                                                      ENA+


                                                                                                                                                                                                                                 ENA-


                                                                                                                                                                                     12                                                                                                    HWMN                    -HBS           -R20120                    411
```

## Página 16

```text
                                                                                                                                                    Hybrid Servo Hardware Installation Manual

PNP (Sourcing) Control Signal Wiring

In this wiring, Pulse, Direction and Enable signal share the same ground (negative) terminal.

                                                                                                  Controller                                                                                                                               Drive
                                                                                                                 VCC                                                VCC = 5-24V

                                                                                                                                                            Pulses                                                      PUL+

                                                                                                                 VCC                                                                                                    PUL-

                                                                                                                                                            Direction                                                   DIR+

                                                                                                                 VCC                                                                                                     DIR-

                                                                                                                                                             Enable                                                    ENA+


                                                                                                                                                                                                                        ENA-


Differential Control Signal Wiring

For the differential output controller, connect to the HBS drive accordingly.

                                                                                                   Controller                                                                                                                              Drive
                                                                                                                                                                    VCC = 5-24V
                                                                                                                            VCC                             Pulses                                                      PUL+


                                                                                                                                                                                                                        PUL-
                                                                                                                            VCC                              Direction                                                  DIR+


                                                                                                                                                                                                                        DIR-
                                                                                                                            VCC                              Enable                                                    ENA+


                                                                                                                                                                                                                       ENA-


                                                                                                                                                                             13                                                                                               HWMN                   -HBS          -R20120                  411
```

## Página 17

```text
                                                                                                                                                                                                                                                                                     Hybrid Servo Hardware Installation Manual

Output Signal Wiring

The HBS drives offers ALM (alarm) signal to indicate the error status. The HBS86 has the in-position
(Pend+ / Pend-) to indicate the achievements of the target position. That is, the motor have been in
the position you want it to be. These signals are OC (Open Collector) output and can sink or source
50mA current.
                                                                                                                                                                                                                                          Controller                                                                                                                                                                                                                                                                                                                           Drive

                                                                                                                                                                                                                                                                                     VCC                                                                                                                   VCC = 5-24V


                                                                                                                                                                                                                                                                                                                                                                                                   Alarm                                                                                                                              ALM+

                                                                                                                                                                                                                                                                                    VCC                                                                                                                                                             R                                                                                ALM-


                                                                                                                                                                                                                                                                                                                                                                                         In-position                                                                                                                                  Pend+


                                                                                                                                                                                                                                                                                                                                                                                                                                                       R                                                                             Pend-


Note: Series resistor R should be added when there is no limit resistor in the controller.

Wiring Notes

l    In order to improve anti-interference performance of the drive, it is recommended to use twisted
                                    pair shield cable.
l      To prevent noise incurred in PUL/DIR signal, pulse/direction signal wires and motor wires should
                                    not be tied up together. It is better to separate them by at least 10 cm, otherwise the disturbing
                                    signals generated by motor will easily disturb pulse direction signals, causing motor position
                                    error, system instability and other failures.
l    If a power supply serves several drives, separately connecting the drives is recommended instead
                                    of daisy-chaining.
l    It is prohibited to pull and plug power connector while the drive is powered ON, because there is
                                    high current flowing through motor coils (even when motor is at standstill). Pulling or plugging
                                    power connector with power on will cause extremely high back-EMF voltage surge, which may
                                    damage the drive.


                                                                                                                                                                                                                                                                                                                                                                                                                                     14                                                                                                                                                                                                                                         HWMN                                                   -HBS                               -R20120                                                       411
```

## Página 18

```text
                                                                                                                                                                                    Hybrid Servo Hardware Installation Manual
Control Signal Setup Timing

To make a reliable operation, the HBS drive requires the control signals to meet the setup time
requirements as follows. Otherwise losing of steps may happen.


                                                                                                                                                                                                                                                                                                                                   Symbol                                    Description
                                                                                                                                                                                                                                                                                                                                             tDS        Direction Setup Time
                                                                                                                                                                                                                                                                                                                                            tPHS        Pulse High Level Setup Time
                                                                                                                                                                                                                                                                                                                                            tPLS         Pulse Low Level Setup Time
                                                                                                                                                                                                                                                                                                                                             tDD        Direction DelayTime
                                                                                                                                                                                                                                                                                                                                              tES         Enable Setup Time
                                                                                                                                                                                                                                                                                                                                             tED         Enable Delay Time


Control Signal Setup Time
                  Drive                           Frequency                                 tDS                    tPHS /     tPLS                      tDD             tES              tED
                HBS57                                  200K                         >50uS                            >2.5us                             >50uS               >200ms                                                                                                                                                                                                                                                                            >200ms
        HBS86(H)                                 200K                         >50uS                            >2.5us                             >50uS               >200ms                                                                                                                                                                                                                                                                                  >200ms

Current Control Detail

Leadshine            ’s hybrid servo motor is integrated with a high-resolution 1,000-line optical incremental
encoder. That encoder can send the real-time shaft position back to the hybrid drive. Like traditional
servo controls, the drive can automatically adjust the output current to the motor. The output
current ranges between the holding current and the close-loop current. When there is no pulse sent
to the drive, the HBS goes into idle mode and the actual motor current is determined by the holding
current percentage (similar to                                                 “idle current                ” of open loop stepper drives). In normal working mode,
the HBS monitors the actual shaft position all the time. The current outputted to the motor changes
dynamically based on the tracking error between the actual position and the commanded position.
Low holding current can reduce motor heating however also reduces the holding torque which is
used to lock the motor shaft at standstill. It is recommended to determine the holding current by
whether or not there is big vibration at start-up and how much lock torque is required, based on your
actual applications.


                                                                                                                                                                                                                                            15                                                                                                                                 HWMN                           -HBS                -R20120                            411
```

## Página 19

```text
                                                                                                                                                                                                                                              Hybrid Servo Hardware Installation Manual
Fine Tuning

Leadshine already loads default current-loop parameters and position-loop parameters. Those
default parameter values have been optimized. They should be good enough for most industrial
applications, and there is no need to tune them. However, if you want to fine tune the IES for best
performance for your applications, Leadshine also offers tuning software, ProTuner, which allows you
to adjust those current-loop and position-loop parameters (see software manual).
Protection Functions

To improve reliability, the HBS incorporates some built-in protection functions. The HBS uses one red
LED to indicate the protection type. The periodic time of red is 4 s (seconds), and the blinking times
of red LED indicates what protection has been activated. Because only one protection can be
displayed by red LED, so the drive will decide what error to display according to their priorities. See
the following protection Indications table for displaying priorities.

       Priority                                                      Time(s) of Blink                                                                                                                                                                                                 Sequence wave of RED LED                                                                         Description


                                                                                                                                                                                                                                                                                                                                    5S
                                                                                                                                                                                           0.2S
                     1st                       1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   Over-current protection


                                                                                                                                                                                                                                                                                                                                                   5S
                                                                                                                                                                                                         0.3S           0.2S
                  2nd                     2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        Over-voltage protection


                                                                                                                                                                                                                                                                                                                                    5S
                                                                                                                                                                                                         0.3S           0.2S
                    3rd                      7                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     Position Following Error


Over-current Protection

Over-current protection will be activated when continuous current exceeds the limit or in case of
short circuit between motor coils or between motor coil and ground, and RED LED will blink once
within each periodic time.

Over-voltage Protection

When power supply voltage exceeds the limits, protection will be activated and red LED will blink
twice within each periodic time.

                                                                                                                               When above protections are active, the motor shaft will be free or the LED will
                                                                                                                               blink. Reset the drive by repowering it to make it function properly after removing
                                                  !                                                                            above problems. Since there is no protection against power leads (                          ﹢,﹣) reversal,
                                     Caution                                                                                   it is critical to make sure that power supply leads correctly connected to drive.
                                                                                                                               Otherwise, the drive will be damaged instantly.

                                                                                                                                                                                                                                                                                                                                                           16                                                                                                                                                                                                HWMN                                         -HBS                         -R20120                                            411
```

## Página 20

```text
                                                                                                                                                                                                                                 Hybrid Servo Hardware Installation Manual

Position Following Error Protection

When the position error exceeds the limit (software configurable, see software manual), position,
protection will be activated and red LED will blink seven times within each periodic time.
Frequently Asked Questions

In the event that your drive doesn                                                 ’t operate properly, the first step is to identify whether the problem
is electrical or mechanical in nature. The next step is to isolate the system component that is causing
the problem. As part of this process you may have to disconnect the individual components that
make up your system and verify that they operate independently. It is important to document each
step in the troubleshooting process. You may need this documentation to refer back to at a later date,
and these details will greatly assist our Technical Support staff in determining the problem should you
need assistance.

Many of the problems that affect motion control systems can be traced to electrical noise, controller
software errors, or mistake in wiring.

Problem Symptoms and Possible Causes

                                                Symptoms                                                                                          Possible Problems
                                                                                                                                                                              No power
                Motor is not rotating                                                                                                                                         Microstep resolution setting is wrong
                                                                                                                                                                              Fault condition exists
                                                                                                                                                                              The drive is disabled
                Motor rotates in the
                wrong direction                                          The Direction signal level is reverse
                                                                                                                                                                              Power supply voltage beyond drive                                                   ’s input range
                The Drive In Fault                                                                                                                                            Something wrong with motor coil
                                                                                                                                                                              Wrong connection
                                                                                                                                                                              Control signal is too weak
                                                                                                                                                                              Control signal is interfered
                Erratic Motor Motion                                                                                                                                          Something wrong with motor coil
                                                                                                                                                                              Motor is undersized for the application
                                                                                                                                                                              Acceleration is set too high
                                                                                                                                                                              Power supply voltage too low
                Excessive motor and                                                                                                                                           Inadequate heat sinking / cooling
                drive heating                                         Load is too high


                                                                                                                                                                                                                                                                                                                                17                                                                                                                                                                                 HWMN                                      -HBS                       -R20120                                        411
```

## Página 21

```text
                                                                                                                                                                                                                                                                                                                                                                                                                             Hybrid Servo Hardware Installation Manual
Warranty

Leadshine Technology Co., Ltd. warrants its products against defects in materials and workmanship
for a period of 12 months from shipment out of factory. During the warranty period, Leadshine will
either, at its option, repair or replace products which proved to be defective.

Exclusions

The above warranty does not extend to any product damaged by reasons of improper or inadequate
handlings by customer, improper or inadequate customer wirings, unauthorized modification or
misuse, or operation beyond the electrical specifications of the product and/or operation beyond
environmental specifications for the product.

Obtaining Warranty Service

To obtain warranty service, a returned material authorization number (RMA) must be obtained from
customer service at e-mail:  before returning product for service. Customer shall prepay shipping
charges for products returned to Leadshine for warranty service, and Leadshine shall pay for return of
products to customer.

Warranty Limitations

Leadshine makes no other warranty, either expressed or implied, with respect to the product.
Leadshine specifically disclaims the implied warranties of merchantability and fitness for a particular
purpose. Some jurisdictions do not allow limitations on how long and implied warranty lasts, so the
above limitation or exclusion may not apply to you. However, any implied warranty of
merchantability or fitness is limited to the 12-month duration of this written warranty.

Shipping Failed Product

If your product fail during the warranty period, e-mail customer service at  to obtain a returned
material authorization number (RMA) before returning product for service. Please include a written
description of the problem along with contact name and address. Send failed product to distributor
in your area or: ULeadshine Technology Co., Ltd. 3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan
Dist, Shenzhen, China.U Also enclose information regarding the circumstances prior to product
failure.


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          18                                                                                                                                                                                                                                                                                                                                                                                           HWMN                                                                                      -HBS                                                     -R20120                                                                                            411
```

## Página 22

```text
                                                                                                                                                     Hybrid Servo Hardware Installation Manual
Contact Us

China Headquarters
Address:            3/F, Block 2, Nanyou Tianan Industrial Park, Nanshan District Shenzhen, China
Web:       http://www.leadshine.com
Sales Hot Line:
Tel:     86-755-2641-7674 (for Asia, Australia, Africa areas)
86-755-2640-9254 (for Europe areas)
86-755-2641-7617 (for America areas)
Fax:     86-755-2640-2718
Email:         sales@leadshine.com                                                                   .

Technical Support:
Tel:     86-755-2641-8447, 86-755-2641-8774, 86-755-2641-0546
Fax:     86-755-2640-2718
Email:         tech@leadshine.com(for                                                                            All)

Leadshine U.S.A
Address:            25 Mauchly, Suite 318 Irvine, California 92618
Tel:     1-949-608-7270
Fax:     1-949-608-7298
Web:       http://www.leadshineUSA.com
Email:         sales@leadshineUSA.com                                                                               and      support@leadshineUSA.com                                                                                     .


                                                                                                                                                                               19                                                                                                 HWMN                   -HBS          -R20120                   411
```

`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company  :   Fundación Fulgor
// Engineer :   Martinez Luciano
// Porject  :   Trabajo Partico N°4
// Module   :   testbench
//////////////////////////////////////////////////////////////////////////////////
// Notas    :
//
// i_sw[3:0]    = b3, b2, b1, b0   
// b3   => habilitador del contador
// b2   => limite de referencia del contador
// b1   => limite de referencia del contador
// b0   => dirección de corrimiento de SR y SR2L
//
// i_btn[3:0]   = b3, b2, b1, b0
// b0   => selector de secuencia
// b1   => selección de color: R
// b2   => selección de color: G
// b3   => selección de color: B
//
// orden de secuencia
// 00   => SR   <= seteo inicial con el reset
// 01   => FS
// 10   => SR2L
//////////////////////////////////////////////////////////////////////////////////

module tb_top();    // no requiere puertos de entrada o salida

    /* parámetros del módulo */
    parameter   n_SW            = 4     ;   // número de bits del selector
    parameter   n_BTN           = 4     ;   // número de bits de los pulsadores
    parameter   n_LEDS          = 4     ;   // número de LEDs de salida
    parameter   n_COUNT         = 13;//32    ;   // número de bits del contador --> 13 para simulación

    /* wire: para conecta señales dentro de un módulo */
    wire        [n_LEDS -1 : 0] o_led       ;   // salida de los LEDs
    wire        [n_LEDS -1 : 0] o_led_r     ;   // salida de los LEDs rojos
    wire        [n_LEDS -1 : 0] o_led_b     ;   // salida de los LEDs azules
    wire        [n_LEDS -1 : 0] o_led_g     ;   // salida de los LEDs verdes

    /* reg: permite almacenar valores en bloques secuenciales y combinacionales <always> */
    reg                         i_clk       ;   // señal de clock
    reg                         i_reset     ;   // señal de reset
    reg         [n_SW   -1 : 0] i_sw        ;   // señal de los selectores
    reg         [n_BTN  -1 : 0] i_btn       ;   // señal de los pulsadores


    top
        /* parametrización */
        #(
            .n_SW            (n_SW      )   ,   // cantidad de bits de los selectores 
            .n_BTN           (n_BTN     )   ,   // cantidad de bits de los pulsadores 
            .n_LEDS          (n_LEDS    )   ,   // cantidad de bits de los leds 
            .n_COUNT         (n_COUNT   )       // cantidad de bits del contador
        )
        u_top
        /* entradas y salidas */
        (
            .i_clk           (i_clk     )   ,   // entrada de clock
            .i_reset         (i_reset   )   ,   // entrada de reset
            .i_sw            (i_sw      )   ,   // entrada de los interruptores (selectores)
            .i_btn           (i_btn     )   ,   // entrada de los pulsadores
            
            .o_led           (o_led     )   ,   // salida de los leds
            .o_led_r         (o_led_r   )   ,   // salida de los leds rojos
            .o_led_g         (o_led_g   )   ,   // salida de los leds verdes
            .o_led_b         (o_led_b   )       // salida de los leds azules
        );

    /* inicialización de variables */
    initial begin
        
        i_clk   = 1'b0      ;   // inicializa la señal de clock a 0
        i_sw    = 4'b0000   ;   // inicializa la señal de selectores a 0000 
        i_btn   = 4'b0000   ;   // inicializa la señal de pulsadores a 0000 
        i_reset = 1'b0      ;   // inicializa la señal de reset a 0
        
        #50
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_reset = 1'b1      ;   // apaga el reset (logica negativa)


        /* testeo de secuencias */
        // secuencia 1
        #50
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_sw    = 4'b0011   ;   // count habilitado | limit_ref = 01
        i_btn   = 4'b0011   ;   // cambia de secuencia a FS 
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador
        
        // secuencia 2
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_btn   = 4'b0001   ;   // cambia de secuencia a SR2L 
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador
        
        // secuencia 3
        #1000   
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo       
        i_btn   = 4'b0001   ;   // cambia de secuencia SR
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador


        /* reset: para diferenciar pruebas */
        #50
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_reset = 1'b0      ;   // inicializa la señal de reset a 0
        
        #500
        @(posedge i_clk)    ;   // espera 500 unidades de tiempo
        i_reset = 1'b1      ;   // apaga el reset (logica negativa)

        

        /* testeo de habilitador del contador */
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b0010   ;   // count deshabilitado | limit_ref = 01

        /* testeo de limite de referencia */
        // limite de referencia R0
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b0001   ;   // count habilitado | limit_ref = 00      

        // limite de referencia R1
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b0011   ;   // count habilitado | limit_ref = 01      
        
        // limite de referencia R2
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b0101   ;   // count habilitado | limit_ref = 10      
        
        // limite de referencia R3
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b0111   ;   // count habilitado | limit_ref = 11      
        

        /* reset: para diferenciar pruebas */
        #50
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_reset = 1'b0      ;   // inicializa la señal de reset a 0
        
        #500
        @(posedge i_clk)    ;   // espera 500 unidades de tiempo
        i_reset = 1'b1      ;   // apaga el reset (logica negativa)



        /* testeo de dirección */
        // secuencia SR     <= seleccionada anteriormente
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b1001   ;   // cambia la dirección => izquierda

        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b0001   ;   // cambia la dirección => derecha

        // cambio de secuencia a SR2L   <= seleccionada
        #1000               
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo       
        i_btn   = 4'b0001   ;   // cambia de secuencia FS
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador

        #5               
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo       
        i_btn   = 4'b0001   ;   // cambia de secuencia FS
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador

        // testeo de dirección 
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b1001   ;   // cambia la dirección => afuera

        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_sw    = 4'b0001   ;   // cambia la dirección => centro


        /* reset: para diferenciar pruebas */
        #50
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_reset = 1'b0      ;   // inicializa la señal de reset a 0
        
        #500
        @(posedge i_clk)    ;   // espera 500 unidades de tiempo
        i_reset = 1'b1      ;   // apaga el reset (logica negativa)


        /* testeo de color: RGB */
        // color R
        #1000
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_sw    = 4'b0011   ;   // count habilitado | limit_ref = 01
        i_btn   = 4'b0010   ;   // cambio de color: R 
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador
        
        // color G
        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_btn   = 4'b0100   ;   // cambio de color: G 
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador
        
        // color B
        #1000   
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo       
        i_btn   = 4'b1000   ;   // cambio de color: B
        
        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador


        /* reset: para diferenciar pruebas */
        #50
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_reset = 1'b0      ;   // inicializa la señal de reset a 0
        
        #500
        @(posedge i_clk)    ;   // espera 500 unidades de tiempo
        i_reset = 1'b1      ;   // apaga el reset (logica negativa)


        /* pruba combinatoria */
        #50
        @(posedge i_clk)    ;   // espera 50 unidades de tiempo
        i_sw    = 4'b0111   ;   // dir = Derecha | limit_ref = R3 | count = Habilitado
        i_btn   = 4'b1011   ;   // color R y B | cambio de secuencia a FS

        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador

        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_btn   = 4'b0001   ;   // cambio de secuencia a SR2L

        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador

        #1000   
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo       
        i_btn   = 4'b1110   ;   // cambio de color: RGB

        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador

        #1000
        @(posedge i_clk)    ;   // espera 1000 unidades de tiempo
        i_btn   = 4'b0001   ;   // cambio de secuencia a SR

        #5
        @(posedge i_clk)    ;   // espera 5 unidades de tiempo
        i_btn   = 4'b0000   ;   // apaga la señal del pulsador


        // Esperar 10000 unidades de tiempo y terminar la simulación
        #10000              ;
        $finish             ;
    end

    // bloque always para genera la señal de clock
    always #5 begin
        // inverte el valor de la señal de clock cada 5 unidades de tiempo
        i_clk = ~i_clk;
    end


endmodule


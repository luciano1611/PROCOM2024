`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company  :   Fundación Fulgor
// Engineer :   Martinez Luciano
// Porject  :   Trabajo Partico N°4
// Module   :   "top"
//////////////////////////////////////////////////////////////////////////////////

/* para implementación en FPGA remota descomentar lo siguiente */
//`define USE_VIO_ILA     // para implementación en FPGA remota <uso de VIO e ILA>

module top
    /* parametrización */
    #(
        parameter   n_SW            = 4             ,   // cantidad de bits de los selectores 
        parameter   n_BTN           = 4             ,   // cantidad de bits de los pulsadores 
        parameter   n_LEDS          = 4             ,   // cantidad de bits de los leds 
        parameter   n_COUNT         = 32                // cantidad de bits del contador
    )
    /* entradas y salidas */
    (
        

    /* para implementación en FPGA remota */
    `ifdef USE_VIO_ILA
        // solo se usa el puerto del clock
        input                       i_clk               // entrada de clock

    /* para simulación con archivo de testbench */
    `else
        // usa todos los puertos
        input                       i_clk           ,   // entrada de clock
        input                       i_reset         ,   // entrada de reset
        input       [n_SW   -1 : 0] i_sw            ,   // entrada de los interruptores (selectores)
        input       [n_BTN  -1 : 0] i_btn           ,   // entrada de los pulsadores
        
        output      [n_LEDS -1 : 0] o_led           ,   // salida de los leds conectados a los pulsadores
        output      [n_LEDS -1 : 0] o_led_r         ,   // salida de los leds rojos     R
        output      [n_LEDS -1 : 0] o_led_g         ,   // salida de los leds verdes    G
        output      [n_LEDS -1 : 0] o_led_b             // salida de los leds azules    B
    `endif
    );

    /* para implementación en FPGA en forma remota */
    `ifdef USE_VIO_ILA

        /* declaración de las conexiones con los modulos de VIO e ILA */
        wire                        i_reset         ;   // probe_out_0  [0:0]
        wire        [n_SW   -1 : 0] i_sw            ;   // probe_out_1  [3:0]
        wire        [n_BTN  -1 : 0] i_btn           ;   // probe_out_2  [3:0]
        
        wire        [n_LEDS -1 : 0] o_led           ;   // probe_in_0   [3:0]
        wire        [n_LEDS -1 : 0] o_led_r         ;   // probe_in_1   [3:0]
        wire        [n_LEDS -1 : 0] o_led_g         ;   // probe_in_2   [3:0]
        wire        [n_LEDS -1 : 0] o_led_b         ;   // probe_in_3   [3:0]

        /* instanciación de los modulos de VIO e ILA */
        vio
        u_vio
            (
                .clk_0              (i_clk)         ,   // 
                .probe_in0_0        (o_led)         ,   // 
                .probe_in1_0        (o_led_r)       ,   // 
                .probe_in2_0        (o_led_g)       ,   // 
                .probe_in3_0        (o_led_b)       ,   // 
                .probe_out0_0       (i_reset)       ,   // 
                .probe_out1_0       (i_sw)          ,   // 
                .probe_out2_0       (i_btn)             // 
            );

        ila
        u_ila
            (
                .clk_0              (i_clk)         ,   // 
                .probe0_0           (o_led)         ,   // 
                .probe1_0           (o_led_r)       ,   // 
                .probe2_0           (o_led_g)       ,   // 
                .probe3_0           (o_led_b)           // 
            );
    `endif 
    
    /* wire: para conecta señales dentro de un módulo o entre modulos */
    wire                            valid           ;   // salida de modulo del contador de enable para el SR y/o FS
    wire            [n_LEDS -1 : 0] led_SR          ;   // salida del modulo SR de los leds     <shift_register>
    wire            [n_LEDS -1 : 0] led_FS          ;   // salida del modulo FS de los leds     <flash>
    wire            [n_LEDS -1 : 0] led_SR2L        ;   // salida del modulo SR2L de los leds   <shift_reg2leds>

    /* reg: permite almacenar valores en bloques secuenciales y combinacionales <always> */
    reg             [n_LEDS -1 : 0] led             ;   // para seleccionar la salida SR, FS o SR2L
    reg             [n_BTN  -1 : 0] prevBtn         ;   // para almacenar el estado previo de los pulsadores
    reg             [n_BTN  -2 : 0] btn             ;   // para almacenar la lectura del pulsador para selección del color de los leds
    reg             [1         : 0] count           ;   // contador para cambiar entre las funciones SR, FS, SR2L

    /* instanciación de los modulos */
    // [1]: modulo del contador
    counter
        /* parametrización */
        #(
            .n_SW           (n_SW -1)               ,   // cantidad de bits del selector
            .n_COUNT        (n_COUNT)                   // cantidad de bits del contador
        )
        u_counter
        /* entradas y salidas del modulo */
        (
            .i_clk          (i_clk)                 ,   // entrada de clock 
            .i_reset        (~i_reset)              ,   // entrada de reset logica negativa
            .i_sw           (i_sw[n_SW -2 : 0])     ,   // entrada de selectores <para el limit_ref del contador> <i_sw[0] para habilitar el contador>
            .o_valid        (valid)                     // salida de enable para el SR y/o FS
        );

    // [2]: modulo del shift register: SR
    shift_register
        /* parametrización */
        #(
            .n_LEDS         (n_LEDS)                    // cantidad de bits de los leds
        )
        u_shift_reg
        /* entradas y salidas del modulo */
        (
            .i_clk          (i_clk)                 ,   // entrada de clock
            .i_reset        (~i_reset)              ,   // entrada de reset logica negativa
            .i_valid        (valid)                 ,   // entrada de enable to shift
            .i_dir          (i_sw[n_SW -1])         ,   // entrada que indica la dirección del corrimiemto: 1'b0 = izquierda : 1'b1 = derecha
            .o_led          (led_SR)                    // salida a los leds
        );

    // [3]: modulo de flash: FS
    flash
        /* parametrización */
        #(
            .n_LEDS         (n_LEDS)                    // cantidad de bits de los leds
        )
        u_flash
        /* entradas y salidas */
        (
            .i_clk          (i_clk)                 ,   // entrada de clock
            .i_reset        (~i_reset)              ,   // entrada de reset logica negativa
            .i_valid        (valid)                 ,   // entrada de enable to flash
            .o_led          (led_FS)                    // salida a los leds
        );

    // [4]: modulo de shift_reg2leds: SR2L: ejecicio B
    shift_reg2leds
    /* parametrización */
        #(
            .n_LEDS         (n_LEDS)                    // cantidad de bits de los leds
        )
        u_shift_reg2led
        (
            .i_clk          (i_clk)                 ,   // entrada de clock
            .i_reset        (~i_reset)              ,   // entrada de reset
            .i_valid        (valid)                 ,   // entrada de enable to shift
            .i_dir          (i_sw[n_SW -1])         ,   // entrada que indica la dirección del corrimiemto: 1'b0 = izquierda : 1'b1 = derecha
            .o_led          (led_SR2L)                  // salida a los leds
        );


    /* always secuencial: lista sencible => señales asincronas de clock y reset */
    always @(posedge i_clk or negedge i_reset) begin
        
        // para: reset == 1
        if (i_reset == 1'b0) begin
            btn                 <= {{n_BTN-2{1'b0}}, 1'b1}  ;   // inicializa btn en 001: Rojo
            prevBtn[n_BTN-1:1]  <= {n_BTN-1{1'b0}}          ;   // inicializa prevBtn en 0       
        end

        // para: i_btn[3:1] distinto de 0
        else if ((i_btn[n_BTN-1:1] != {n_BTN-1{1'b0}}) && (i_btn[n_BTN-1:1] != prevBtn[n_BTN-1:1])) 
            btn             <= i_btn[n_BTN-1 : 1]   ;   // se asigna el valor leido del pulsador a r_btn

        // si no:
        else 
            btn             <= btn                  ;   // se mantiene el valor anterior
        
        prevBtn[n_BTN-1:1]  <= i_btn[n_BTN-1 : 1]   ;   // en cada ciclo se almacena el btn para comparar en el siguiente estado
    end


    /* always secuencial para contador de pulsador i_btn[0] para selección de las salidas: lista sencible => señales asincronas de clock y reset */
    always @(posedge i_clk or negedge i_reset) begin
        // para: reset == 1
        if (i_reset == 1'b0) begin
            count       <= 2'b00    ;   // resetea el contador
            prevBtn[0]  <= 1'b0     ;   // setea en 0 el estado anterior de btn
        end

        // para: una entrada del pulsador i_btn[0] que pasa de 0 a 1: comparando con el estado de btn en el clock anterior
        else if ((i_btn[0] == 1'b1) && (prevBtn[0] == 1'b0)) 

            // para: cuenta de 0 a 2 = 2'b10
            if (count < 2'b10) 
                count   <= count +1     ;   // incremento del contador                
            // si supera el limite
            else
                count   <= 2'b00        ;   // reinicio del contador
        // si no:
        else 
            count       <= count        ;   // se mantiene el valor del contador
    
        prevBtn[0]      <= i_btn[0]     ;   // en cada ciclo se almacena el btn para comparar en el siguiente estado
    end


    /* always combinacional para multiplexor de los leds de salida */
    always @(*) begin
        case(count)
            2'b00   : led <= led_SR      ;   // asignación de la salida del modulo RS a la conexión led con los leds de salida del top level
            2'b01   : led <= led_FS      ;   // asignación de la salida del modulo FS a la conexión led con los leds de salida del top level
            2'b10   : led <= led_SR2L    ;   // asignación de la salida del modulo RS2L a la conexión led con los leds de salida del top level    
            default : led <= led_SR      ;   // asignación de la salida del modulo RS a la conexión led con los leds de salida del top level
        endcase
    end


    /* assignación a los leds de salida */
    assign o_led_r  = (btn[0] == 1'b1) ? led    : {n_LEDS {1'b0}}   ;   // asignación de los leds rojos segun btn[0]
    assign o_led_g  = (btn[1] == 1'b1) ? led    : {n_LEDS {1'b0}}   ;   // asignación de los leds verdes segun btn[1]   
    assign o_led_b  = (btn[2] == 1'b1) ? led    : {n_LEDS {1'b0}}   ;   // asignación de los leds azules segun btn[2]
    assign o_led    = i_btn                                         ;   // asignación de los leds conectados a los pulsadores



endmodule


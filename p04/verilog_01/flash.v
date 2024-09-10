`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company  :   Fundación Fulgor
// Engineer :   Martinez Luciano
// Porject  :   Trabajo Partico N°4
// Module   :   FS ==> "flash"
//////////////////////////////////////////////////////////////////////////////////

module flash
    /* parametrización */
    #(
        parameter   n_LEDS      = 4             // cantidad de bits de los leds
    )
    /* entradas y salidas */
    (
        input                   i_clk       ,   // entrada de clock
        input                   i_reset     ,   // entrada de reset
        input                   i_valid     ,   // entrada de enable to flash
        output  [n_LEDS -1 : 0] o_led           // salida a los leds
    );

    /* reg: permite almacenar valores en bloques secuenciales y combinacionales <always> */ 
    reg         [n_LEDS -1 : 0] flash       ;   // variable para realizar el 


    /* always secuencial <logica secuencial del modo flash>: lista sencible => señales asincronas de clock y reset */ 
    always @(posedge i_clk or posedge i_reset) begin
        
        // para: reset == 1 
        if (i_reset == 1'b1) 
            flash   <= {n_LEDS {1'b1}}  ;   // 4'b1111
        
        // para: enable == 1 
        else if (i_valid == 1'b1) 
            flash   <= ~flash           ;   // se togglea la señal de los leds
        
        // si no: 
        else 
            flash   <= flash            ;   // se mantiene el valor que habia en el clock anterior
    end

    // asignación del valor del r_flash a la salida de los leds  
    assign  o_led   = flash             ;   

endmodule

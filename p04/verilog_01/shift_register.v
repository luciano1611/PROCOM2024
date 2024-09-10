`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company  :   Fundación Fulgor
// Engineer :   Martinez Luciano
// Porject  :   Trabajo Partico N°4
// Module   :   SR ==> "shift_register"
//////////////////////////////////////////////////////////////////////////////////

module shift_register
    /* parametrización */
    #(
        parameter   n_LEDS      = 4             // cantidad de bits de los leds
    )
    /* entradas y salidas del modulo */
    (
        input                   i_clk       ,   // entrada de clock
        input                   i_reset     ,   // entrada de reset
        input                   i_valid     ,   // entrada de enable to shift
        input                   i_dir       ,   // entrada que indica la dirección del corrimiemto: 1'b0 = izquierda : 1'b1 = derecha
        output  [n_LEDS -1 : 0] o_led           // salida a los leds
    );

    /* reg: permite almacenar valores en bloques secuenciales y combinacionales <always> */
    reg         [n_LEDS -1 : 0] shift_reg   ;   // para realizar el corrimiento


    /* always secuencial <logica secuencial del shift register>: lista sencible => señales asincronas de clock y reset */ 
    always @(posedge i_clk or posedge i_reset) begin
        
        // para: reset == 1 
        if (i_reset == 1'b1) 
            shift_reg   <= {{n_LEDS -1 {1'b0}}, 1'b1}           ;   // 4'b0001  
        

        // para: enable to shift == 1: realiza el corrimiento 
        else if (i_valid == 1'b1) begin
            
            // si i_dir == 0: corrimeinto a la derecha 
            if      (i_dir    == 1'b0) begin
                shift_reg              <= shift_reg       >> 1  ;   // 1 corrimeinto a la derecha
                shift_reg [n_LEDS -1]  <= shift_reg [0]         ;   // asignación del LSB al MSB
            end
            
            // si i_dir == 1: corrimeinto a la izquierda 
            else if (i_dir    == 1'b1) begin
                shift_reg              <= shift_reg        << 1 ;   // 1 corrimeinto a la izquierda
                shift_reg[0]           <= shift_reg [n_LEDS -1] ;   // asignación del MSB al LSB
            end
        end
        
        // si no: mantiene el valor anterior
        else
            shift_reg                  <= shift_reg           ;   
    end

    // asignación del valor de la variable shift_reg a la salida a los leds
    assign  o_led       = shift_reg    ;

endmodule

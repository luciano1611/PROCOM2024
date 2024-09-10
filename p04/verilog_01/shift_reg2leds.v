`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company  :   Fundación Fulgor
// Engineer :   Martinez Luciano
// Porject  :   Trabajo Partico N°4
// Module   :   SR2L ==> "shift_reg2leds"
//////////////////////////////////////////////////////////////////////////////////

module shift_reg2leds
    /* parametrización */
    #(
        parameter n_LEDS    = 4                 // cantidad de bits de los leds
    )
    
    (
        input                   i_clk       ,   // entrada de clock
        input                   i_reset     ,   // entrada de reset
        input                   i_valid     ,   // entrada de enable to shift
        input                   i_dir       ,   // entrada que indica la dirección del corrimiemto: 1'b0 = izquierda : 1'b1 = derecha
        output  [n_LEDS -1 : 0] o_led           // salida a los leds
    );

    /* localparam: define una constante de solo lectura dentro del modulo */
    localparam  N = (n_LEDS/2)              ;   // tamaño de registros auxiliares para realizar el corrimiento 3-bits

    /* reg: permite almacenar valores en bloques secuenciales y combinacionales <always> */
    reg         [N : 0]         ms_reg      ;   // registro axiliar con la parte mas significativa 
    reg         [N : 0]         ls_reg      ;   // registro axiliar con la parte menos significativa

    /* always secuencial: lista sencible => señales asincronas de clock y reset */
    always @(posedge i_clk or posedge i_reset) begin

        // para reset = 1
        if (i_reset == 1'b1) begin 
            // inicialización con 6'b001_100 
            ms_reg <= {{N{1'b0}}    , 1'b1     }    ;   // 3'b001            
            ls_reg <= {1'b1         , {N{1'b0}}}    ;   // 3'b100
        end

        // para valid = 1
        else if(i_valid == 1'b1) begin

            // para dir = 0: corrimiento al centro:         >> <<
            if (i_dir == 1'b0) begin
                ms_reg  <= (ms_reg[0]) ? {1'b1      , {N{1'b0}}} : ms_reg >> 1 ;    // 3'b100
                ls_reg  <= (ls_reg[N]) ? {{N{1'b0}} , 1'b1     } : ls_reg << 1 ;    // 3'b001
            end

            // para dir = 1: corrimiento a los extremos:    << >>
            else begin
                ms_reg  <= (ms_reg[N]) ? {{N{1'b0}} , 1'b1     } : ms_reg << 1 ;    // 3'b001
                ls_reg  <= (ls_reg[0]) ? {1'b1      , {N{1'b0}}} : ls_reg >> 1 ;    // 3'b100
            end
        end

        // si no: mantienen los valores
        else begin
            ms_reg      <= ms_reg   ;
            ls_reg      <= ls_reg   ;
        end
    end

    // assignación a los leds de salida del modulo por concatenación: 
    assign o_led    = { ms_reg[N : 1], ls_reg[N-1 : 0]}   ;   // se desprecian el LSB del MS_REG y el MSB del LS_REG
endmodule


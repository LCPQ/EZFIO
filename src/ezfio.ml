(*
    EZFIO is an automatic generator of I/O libraries
    Copyright (C) 2009 Anthony SCEMAMA, CNRS
 
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 
    Anthony Scemama
    LCPQ - IRSAMC - CNRS
    Universite Paul Sabatier
    118, route de Narbonne      
    31062 Toulouse Cedex 4      
    scemama@irsamc.ups-tlse.fr
*)

(*$HEAD*)

(*
Exceptions
==========
*)

exception Read_only of string;;

(*
State variables
===============
*)
let read_only = ref false;;
let ezfio_filename = ref "EZFIO_File";;

(* 
Helper functions
=================
*)

let check_readonly =
  if !read_only then
    raise (Read_only "Read only attribute is set");
;;

let exists path =
  let filename = path^"/.version" in
  Sys.file_exists filename
;;
 
let has group name =
  let dirname = !ezfio_filename ^ "/" ^ group in
  if (exists dirname) then
    (Sys.file_exists (dirname ^ "/" ^ name) )
  else
    false
;;

let has_array group name = has group (name^".gz");;

let mkdir path =
  check_readonly;
  if (exists path) then
    raise (Failure (path^" already exists"));
  Unix.mkdir path 0o777;
  let out_channel = open_out (path^"/.version") in
  Printf.fprintf out_channel "%s\n" version ;
  close_out out_channel;
;;

let create_group group =
  let dirname = !ezfio_filename ^ "/" ^ group in
  if not (exists dirname) then
      mkdir dirname;
;;

let split line s = 
  let rec do_work lst word = function
  | 0 -> word::lst
  | i -> 
    begin
      match line.[i-1] with
      | a when a == s ->
        if word <> "" then 
           do_work (word::lst) "" (i-1) 
        else
           do_work lst "" (i-1) 
      | a -> do_work lst ( (Char.escaped a)^word) (i-1)
    end
  in do_work [] "" (String.length line) 
;;

let ltrim s =
  let rec do_work s l = 
  match s.[0] with
  | '\n' 
  | ' ' -> do_work (String.sub s 1 (l-1)) (l-1)
  | _ -> s
  in
  do_work s (String.length s)
;;

let rtrim s =
  let rec do_work s l = 
  let newl = l-1 in
  match s.[newl] with
  | '\n'
  | ' ' -> do_work (String.sub s 0 (newl)) (newl)
  | _ -> s
  in
  do_work s (String.length s)
;;

let trim s = ltrim (rtrim s) ;;

let maxval l = 
  match l with
  | [] -> None
  | [a] -> Some a
  | hd::tail -> Some (List.fold_left max hd tail)
;;

let minval l = 
  match l with
  | [] -> None
  | [a] -> Some a
  | hd::tail -> Some (List.fold_left min hd tail)
;;

let at arr idx = arr.(idx);;

let size (_) = 0;;

let n_count_ch (str,_,v) =
  let rec do_work accu = function
  | 0 -> accu
  | i -> 
    let newaccu = 
      if str.[i-1] == v then accu+1
      else accu 
    in do_work newaccu (i-1)
  in do_work 0 (String.length str)
;;

let n_count (l,_,v) =
  let rec do_work accu = function
  | []  -> accu
  | h::tail -> 
    let newaccu = 
      if h == v then accu+1
      else accu 
    in do_work newaccu tail
  in do_work 0 l
;;

(* 
Scalars
=======
*)

(*
Read
----
*)

let read_scalar type_conversion group name =
  let in_filename = !ezfio_filename ^ "/" ^ group ^ "/" ^ name in
  let in_channel = open_in in_filename in
  let trimmed_line = trim (input_line in_channel) in
  let result = type_conversion trimmed_line in
  begin
    close_in in_channel ;
    result
  end
;;

let fortran_bool_of_string = function
  | "T" | "t" -> true
  | "F" | "f" -> false
  | x -> raise (Failure ("fortran_bool_of_string should be T or F: "^x))
;;

let fortran_string_of_bool = function
 | true -> "T\n"
 | false-> "F\n"
;;

let read_int   = read_scalar   int_of_string ;;
let read_float = read_scalar float_of_string ;;
let read_string= read_scalar (fun (x:string) -> x);;
let read_bool  = read_scalar fortran_bool_of_string;;

(*
Write
-----
*)

let print_int out_channel i = Printf.fprintf out_channel "%16d\n" i
and print_float out_channel f = Printf.fprintf out_channel "%24.15e\n" f
and print_string out_channel s = Printf.fprintf out_channel "%s\n" s
and print_bool out_channel b = Printf.fprintf out_channel "%s\n" (fortran_string_of_bool b);;

let write_scalar print_fun group name s =
  check_readonly;
  create_group group;
  let out_filename = !ezfio_filename ^ "/" ^ group ^ "/" ^ name in
  let out_channel = open_out out_filename in
  begin
     print_fun out_channel s;
     close_out out_channel;
  end
;;
  
let write_int    = write_scalar print_int
and write_float  = write_scalar print_float
and write_bool   = write_scalar print_bool
and write_string = write_scalar print_string
;;



(*
Arrays
======
*)

type 'a ezfio_data =
| Ezfio_item of 'a array 
| Ezfio_data of ('a ezfio_data) array
;;


type 'a ezfio_array =
{ rank : int ;
  dim  : int array;
  data : 'a ezfio_data ;
}
;;

let ezfio_get_element { rank=r ; dim=d ; data=data } coord =
  (*assert ((List.length coord) == r);*)
  let rec do_work buffer = function
  | [c] -> 
    begin match buffer with
    | Ezfio_item buffer -> buffer.(c)
    | Ezfio_data buffer -> raise (Failure "Error in ezfio_get_element")
    end
  | c::tail -> 
    begin match buffer with
    | Ezfio_item buffer -> raise (Failure "Error in ezfio_get_element")
    | Ezfio_data buffer -> do_work buffer.(c) tail
    end
  | [] -> raise (Failure "Error in ezfio_get_element")
  in
  do_work data coord
;;


let flattened_ezfio_data d = 
  match d with
  | Ezfio_item d -> d
  | Ezfio_data d ->
  let d = Array.to_list d in
  let rec do_work accu = function
  | [] -> accu
  | (Ezfio_item x)::tail -> do_work (Array.append accu x) tail
  | (Ezfio_data x)::tail -> 
    let newaccu = do_work accu (Array.to_list x )
    in  do_work newaccu tail
  in
  do_work (Array.of_list []) d
;;


(*
Read
----
*)

let unzipped_filename filename =
  if not (Sys.file_exists filename) then
    raise (Failure ("file "^filename^" doesn't exist"));
  let uz_filename = Filename.temp_file "" ".tmp" ~temp_dir:(Sys.getcwd ()) in
  let command = "zcat "^filename^" > "^uz_filename
  in
  if (Sys.command command) == 0  then
    uz_filename
  else
    begin
     Sys.remove uz_filename ;
     raise (Failure ("Unable to execute :\n"^command))
    end
;;

let read_rank in_channel =
    let trimmed_line = trim (input_line in_channel) in
    int_of_string trimmed_line 
;;

let read_dimensions in_channel =
    let trimmed_line = trim (input_line in_channel) in
    let list_of_str = split trimmed_line ' ' in
    Array.of_list (List.map int_of_string list_of_str)
;;


let read_array type_conversion group name : 'a ezfio_array =
  let in_filename = !ezfio_filename ^ "/" ^ group ^ "/" ^ name ^ ".gz" in
  let uz_filename = unzipped_filename in_filename in
  let in_channel = open_in uz_filename in
  (* Read rank *)
  let rank = read_rank in_channel 
  (* Read dimensions *)
  and dimensions = read_dimensions in_channel 
  in
  begin
      assert (rank == Array.length dimensions) ;
      (* Read one-dimensional arrays *)
      let read_1d nmax = 
        let rec do_work accu = function
        | 0 -> Array.of_list (List.rev accu)
        | n -> 
          let trimmed_line = trim (input_line in_channel) in
          do_work ( (type_conversion trimmed_line)::accu ) (n-1)
        in
        Ezfio_item (do_work [] nmax)
      in
      (* Read multi-dimensional arrays *)
      let rec read_nd = function
        | m when m<1 -> raise (Failure "dimension should not be <1")
        | 1 -> read_1d dimensions.(0)
        | m -> 
          let rec do_work accu = function
          | 0 -> Array.of_list (List.rev accu)
          | n -> 
            let newlist = read_nd (m-1) in
            do_work (newlist::accu) (n-1)
          in
          Ezfio_data (do_work [] dimensions.(m-1))
      in
      let result = {
         rank = rank ;
         dim = dimensions ;
         data = read_nd rank ;
      } 
      in
      close_in in_channel ;
      Sys.remove uz_filename ;
      result;
  end
;;
  
let read_int_array    = read_array          int_of_string
and read_float_array  = read_array        float_of_string
and read_bool_array   = read_array fortran_bool_of_string
and read_string_array = read_array (fun (x:string) -> x)
;;

(*
Write
-----
*)

let write_array print_fun group name a =
  check_readonly;
  create_group group;
  let out_filename = !ezfio_filename ^ "/" ^ group ^ "/" ^ name ^".gz" in
  let uz_filename = Filename.temp_file "" ".tmp" ~temp_dir:(Sys.getcwd ()) in
  let out_channel = open_out uz_filename in
  let { rank=rank ; dim=dimensions ; data=data } = a in
  let data = flattened_ezfio_data data 
  in
  begin
     (* Write rank *)
     Printf.fprintf out_channel "%4d\n" rank;
     (* Write dimensions *)
     Array.iter (Printf.fprintf out_channel " %8d") dimensions;
     Printf.fprintf out_channel "\n";
     Array.iter (print_fun out_channel) data;
     close_out out_channel ;
     let command = "gzip -c < "^uz_filename^" > "^out_filename
     in
     if (Sys.command command == 0) then (Sys.remove uz_filename )
     else raise (Failure ("command failed:\n"^command))
  end
;;

let write_int_array    = write_array print_int
and write_float_array  = write_array print_float
and write_string_array = write_array print_string
and write_bool_array   = write_array print_bool;;

(*
Library routines
*)

let set_file filename =
  if not (exists filename) then
  begin
    mkdir filename;
    mkdir (filename^"/ezfio");
    let command = Printf.sprintf "
      LANG= date > %s/ezfio/creation
      echo $USER > %s/ezfio/user
      echo %s > %s/ezfio/library" filename filename library filename
    in
    if (Sys.command command <> 0) then
      raise (Failure ("Unable to create new ezfio file:\n"^filename))
  end ;
  ezfio_filename := filename
;;


(*$TAIL*)

 
 let is_prime n =
    let n = abs n in
    let rec is_not_divisor d =
      d * d > n || (n mod d <> 0 && is_not_divisor (d + 1)) in
    n <> 1 && is_not_divisor 2;;
    
    
# (* Build all trees with given [left] and [right] subtrees. *)
  let add_trees_with left right all =
    let add_right_tree all l =
      List.fold_left (fun a r -> Node ('x', l, r) :: a) all right in
    List.fold_left add_right_tree all left
  
  let rec cbal_tree n =
    if n = 0 then [Empty]
    else if n mod 2 = 1 then
      let t = cbal_tree (n / 2) in
      add_trees_with t t []
    else (* n even: n-1 nodes for the left & right subtrees altogether. *)
      let t1 = cbal_tree (n / 2 - 1) in
      let t2 = cbal_tree (n / 2) in
      add_trees_with t1 t2 (add_trees_with t2 t1 []);;
      
      let rec count_leaves = function
    | Empty -> 0
    | Node (_, Empty, Empty) -> 1
    | Node (_, l, r) -> count_leaves l + count_leaves r;;

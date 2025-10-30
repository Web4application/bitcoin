// This is a generated Motoko binding.
// Please use `import service "ic:canister_id"` instead to call canisters on the IC if possible.

module {
  public type AddCanisterRequest = {
    arg : Blob;
    initial_cycles : Nat64;
    wasm_module : Blob;
    name : Text;
    memory_allocation : ?Nat;
    compute_allocation : ?Nat;
  };
  public type CanisterAction = { #Start; #Stop };
  public type CanisterIdRecord = { canister_id : Principal };
  public type CanisterInstallMode = { #reinstall; #upgrade; #install };
  public type CanisterSettings = {
    freezing_threshold : ?Nat;
    wasm_memory_threshold : ?Nat;
    controllers : ?[Principal];
    reserved_cycles_limit : ?Nat;
    log_visibility : ?LogVisibility;
    wasm_memory_limit : ?Nat;
    memory_allocation : ?Nat;
    compute_allocation : ?Nat;
  };
  public type CanisterStatusLogVisibility = {
    #controllers;
    #public_;
    #allowed_viewers : [Principal];
  };
  public type CanisterStatusResult = {
    memory_metrics : ?MemoryMetrics;
    status : CanisterStatusType;
    memory_size : Nat;
    cycles : Nat;
    settings : DefiniteCanisterSettings;
    query_stats : ?QueryStats;
    idle_cycles_burned_per_day : ?Nat;
    module_hash : ?Blob;
    reserved_cycles : ?Nat;
  };
  public type CanisterStatusType = { #stopped; #stopping; #running };
  public type ChangeCanisterControllersError = {
    code : ?Int32;
    description : Text;
  };
  public type ChangeCanisterControllersRequest = {
    target_canister_id : Principal;
    new_controllers : [Principal];
  };
  public type ChangeCanisterControllersResponse = {
    change_canister_controllers_result : ChangeCanisterControllersResult;
  };
  public type ChangeCanisterControllersResult = {
    #Ok;
    #Err : ChangeCanisterControllersError;
  };
  public type ChangeCanisterRequest = {
    arg : Blob;
    wasm_module : Blob;
    stop_before_installing : Bool;
    mode : CanisterInstallMode;
    canister_id : Principal;
    chunked_canister_wasm : ?ChunkedCanisterWasm;
  };
  public type ChunkedCanisterWasm = {
    wasm_module_hash : Blob;
    chunk_hashes_list : [Blob];
    store_canister_id : Principal;
  };
  public type DefiniteCanisterSettings = {
    freezing_threshold : ?Nat;
    wasm_memory_threshold : ?Nat;
    controllers : [Principal];
    reserved_cycles_limit : ?Nat;
    log_visibility : ?CanisterStatusLogVisibility;
    wasm_memory_limit : ?Nat;
    memory_allocation : ?Nat;
    compute_allocation : ?Nat;
  };
  public type LogVisibility = { #controllers; #public_ };
  public type MemoryMetrics = {
    wasm_binary_size : ?Nat;
    wasm_chunk_store_size : ?Nat;
    canister_history_size : ?Nat;
    stable_memory_size : ?Nat;
    snapshots_size : ?Nat;
    wasm_memory_size : ?Nat;
    global_memory_size : ?Nat;
    custom_sections_size : ?Nat;
  };
  public type QueryStats = {
    response_payload_bytes_total : ?Nat;
    num_instructions_total : ?Nat;
    num_calls_total : ?Nat;
    request_payload_bytes_total : ?Nat;
  };
  public type StopOrStartCanisterRequest = {
    action : CanisterAction;
    canister_id : Principal;
  };
  public type UpdateCanisterSettingsError = {
    code : ?Int32;
    description : Text;
  };
  public type UpdateCanisterSettingsRequest = {
    canister_id : Principal;
    settings : CanisterSettings;
  };
  public type UpdateCanisterSettingsResponse = {
    #Ok;
    #Err : UpdateCanisterSettingsError;
  };
  public type Self = actor {
    add_nns_canister : shared AddCanisterRequest -> async ();
    canister_status : shared CanisterIdRecord -> async CanisterStatusResult;
    change_canister_controllers : shared ChangeCanisterControllersRequest -> async ChangeCanisterControllersResponse;
    change_nns_canister : shared ChangeCanisterRequest -> async ();
    get_build_metadata : shared query () -> async Text;
    stop_or_start_nns_canister : shared StopOrStartCanisterRequest -> async ();
    update_canister_settings : shared UpdateCanisterSettingsRequest -> async UpdateCanisterSettingsResponse;
  }
}
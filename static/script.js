async function calculateInstant() {

    let formData = new FormData();

    document.querySelectorAll(".live-input").forEach(input => {
        formData.append(input.name, input.value);
    });

    let res = await fetch("/calculate", {
        method: "POST",
        body: formData
    });

    let data = await res.json();

    if (data.status === "success") {
        let r = data.results;

        document.getElementById("feed_flow").innerText = r.feed_flow ?? "";
        document.getElementById("feed_pump_capacity").innerText = r.feed_pump_capacity ?? "";
        document.getElementById("no_of_membranes").innerText = r.no_of_membranes ?? "";
        document.getElementById("no_of_membranes_in_ceil").innerText = r.no_of_membranes_in_ceil ?? "";
        document.getElementById("backwash_pump_capacity").innerText = r.backwash_pump_capacity ?? "";
        document.getElementById("CEB_pump_flow_rate").innerText = r.CEB_pump_flow_rate ?? "";

        document.getElementById("caustic_dosing_pump_capacity").innerText = r.caustic_dosing_pump_capacity ?? "";
        document.getElementById("hcl_dosing_pump_capacity").innerText = r.hcl_dosing_pump_capacity ?? "";
        
        document.getElementById("naOCI_dosing_pump_capacity").innerText = r.naOCI_dosing_pump_capacity ?? "";
        document.getElementById("cip_pump_capacity_skid").innerText = r.cip_pump_capacity_skid ?? "";

    }
}


// Attach event listener to every input field
document.querySelectorAll(".live-input").forEach(input => {
    input.addEventListener("input", calculateInstant);
});

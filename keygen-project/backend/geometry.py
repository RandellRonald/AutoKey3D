import cadquery as cq
import os
from cadquery import exporters

# CONSTANTS - All dimensions in millimeters
BLADE_LENGTH = 22.0
BLADE_WIDTH = 8.0
BLADE_THICKNESS = 2.3
CUT_SPACING = 3.0

def build_stl(cuts: list[float], hash_val: str) -> str:
    """
    Generates a 3D model of the key based on cut depths.
    Returns the relative path to the generated STL file.
    """
    
    # 1. Create Base Blade: Rectangular solid (22 x 8 x 2.3)
    # Centered at (0,0,0) helps, but let's position it logically.
    # Let's align the spine of the key (the uncut side) or the center.
    # We'll create a box.
    base = cq.Workplane("XY").box(BLADE_LENGTH, BLADE_WIDTH, BLADE_THICKNESS)
    
    # 2. Apply Cuts
    # The cuts are triangular subtractions along one edge.
    # We need to position the cuts correctly.
    # Spacing is 3mm centers.
    # Where does the first cut start? The prompt says "along one edge".
    # Assuming standard key geometry, cuts start from the tip or shoulder.
    # Let's assume the first cut is at some offset or starts from one end.
    # Given "Spacing: 3mm centers", let's assume the first cut is at X = 3mm (or 0 + offset).
    # Based on user comment: "x = i * CUT_SPACING".
    # And we assume the blade spans from X=0 to X=22 or similar.
    # Let's verify coordinates.
    # If using box(), the center is at (0,0,0).
    # Length is X (22), Width is Y (8), Thickness is Z (2.3).
    # X range: -11 to 11.
    # Y range: -4 to 4.
    # Z range: -1.15 to 1.15.
    
    # To make "x = i * CUT_SPACING" intuitive, let's translate the base so X starts at 0.
    # And Y edge is at +4 or -4.
    
    # Let's create the base such that the corner is at (0,0,0) or convenient logic.
    # Better: Use workplane center, but calculate cut positions carefully.
    
    # Let's model the cutter.
    # Cuts are triangular. "Depth from cut array".
    # A standard key cut is a V-shape.
    # 90 degrees or fixed angle?
    # Usually 90-105 degrees. Let's start with a standard V.
    # Since only depth is specified, let's assume a reasonable width for the V at the top.
    # Or, the depth is the primary constraint.
    # "6 triangular subtractions".
    
    # Let's work on the "Front" or "Top" face logic.
    # Let's align blade so Length is along X.
    
    # To match user comment "x = i * CUT_SPACING", let's assume i is 1-indexed or 0-indexed with offset.
    # 6 cuts. 22mm length. 6 * 3 = 18mm required.
    # Leaves 4mm for tip/shoulder.
    # Let's start first cut at X=2mm or X=3mm from the "head" (shoulder) end.
    # Let's assume the cuts go into the blade width (Y axis).
    
    # Approach:
    # 1. Create base.
    # 2. Loop through cuts.
    # 3. For each cut, create a triangular prism (Cut shape).
    # 4. Cut it from the base.
    
    result = base
    
    # Let's adjust coordinate system for easier math.
    # Move base so X=0 is the start of the blade (shoulder).
    # Y=0 is the center line. Y=+4 is the top edge (where we cut).
    # Z=0 is center.
    
    # Since cq.Workplane.box creates centered at origin:
    # X is [-11, 11]. Y is [-4, 4].
    # Let's say cuts are along Y=+4 edge.
    # Cut positions along X. 
    # Let's map cuts[0] to the first position.
    # If we iterate 0 to 5.
    # Position X? 
    # Let's try starting from the "shoulder" which implies near the head.
    # Assuming X=-11 is shoulder, X=11 is tip.
    # i=0 -> cut 1. distance from shoulder.
    # Let's use x = (i+1) * CUT_SPACING relative to the start?
    # Or start at X = -11 + offset.
    # Let's assume offset is some small margin, say 2mm.
    # NOTE: User comment "x = i * CUT_SPACING" is a hint.
    # It might mean position relative to some datum.
    # If we assume specific X coords:
    # Let's assume the cut centers are at X = (i * 3) + Offset.
    # Let's center the cuts properly within the 22mm length.
    # 6 cuts = 5 spaces of 3mm = 15mm span between centers.
    # Placed in 22mm.
    # 22 - 15 = 7mm margin total. 
    # Let's say 3.5mm margin on each side?
    # Or start at 2mm... 
    # Let's use the USER COMPLIANT logic: x = i * CUT_SPACING.
    # Maybe `i` starts at 1?
    # If i=0, x=0. If i=1, x=3...
    # If we align the "start" of the key at X=0.
    # Then cut 0 is at X=0? That cuts the shoulder.
    # Let's assume i starts at certain index or offset.
    # Let's stick to X coordinates on the body:
    # Let's place the blade starting at X=0.
    base = base.translate((BLADE_LENGTH/2, 0, 0)) # Now X is [0, 22]. Y is [-4, 4].
    
    # User comment: "x = i * CUT_SPACING". 
    # Let's assume `i` is the index 0..5.
    # Then x = 0, 3, 6, 9, 12, 15.
    # But X=0 is the very edge. A cut depth at X=0 would slice off the face.
    # Maybe there is an offset? Or `i` starts at 1?
    # Let's assume start offset + i * spacing.
    # A standard key usually has the first cut a few mm from the shoulder.
    # Let's add a `START_OFFSET` of 3.0mm to be safe and use local X relative to that.
    # OR, interpret "x = i * CUT_SPACING" strictly? 
    # If strictly: `x` varies. 
    # Let's assume the cuts are distributed reasonably. 
    # Let's try: cuts at X = 3, 6, 9, 12, 15, 18. (i.e. (i+1)*3).
    # This fits perfectly in 0..22 range (Ends at 18, 4mm tip left).
    # So `x_pos = (i + 1) * CUT_SPACING`.
    
    for i, depth in enumerate(cuts):
        # x_pos along the blade
        x_pos = (i + 1) * CUT_SPACING
        
        # Position: X = x_pos.
        # Y = +4 (edge).
        # We cut INTO the key (Negative Y direction from +4).
        # Depth is how deep it goes from Y=4 towards Y=-4.
        # Tip of the V should be at Y = 4 - depth.
        
        # Create a triangular prism cutter.
        # Shape on XY plane? No, shape on X-Y plane (side view) is triangle.
        # Extruded along Z (Thickness).
        
        # Triangle vertices (Side view):
        # 1. (x_pos, 4 - depth) - The bottom of the cut.
        # 2. (x_pos - width/2, 4) - Top left on edge.
        # 3. (x_pos + width/2, 4) - Top right on edge.
        
        # How wide is the cut?
        # Usually 90 degrees at bottom?
        # If 90 deg, then width/2 = depth. Width = 2*depth.
        # This is a solid assumption for parametric keys.
        # Or fixed width? Fixed width might make shallow cuts look weird or deep cuts overlap.
        # Adjacent spacing is 3mm.
        # Max depth 2.5mm.
        # If 90 deg, deep cut (2.5) has half-width 2.5. Total width 5.0.
        # Centers are 3.0 apart.
        # 5.0 width means overlap with neighbors (Overlap radius 2.5 vs distance 3.0).
        # Since 2.5 < 3.0, the TIP of one cut won't reach the center of the next.
        # But the tops will merge. This is normal for keys (serrated edge).
        # We need to union the cutters or subtract them sequentially.
        # Verify "Adjacent cut difference <= 1.5mm".
        # This prevents extreme slopes.
        
        # Let's use angle of 100 degrees or just 90 degrees (depth = half_width).
        half_width = depth * 1.0 # 90 degree V
        
        # Define vertices for the prism face on the XY plane
        p1 = (x_pos, 4.0 - depth) # Tip
        p2 = (x_pos - half_width, 4.05) # Top Left (slightly above 4 to ensure clean cut)
        p3 = (x_pos + half_width, 4.05) # Top Right
        
        # We need to make this a solid logic.
        # Make a wire and extrude.
        # Face is on XY plane? Yes.
        # Extrude along Z.
        # Need to ensure it cuts through full thickness (-1.15 to 1.15).
        # Extrude large amount centered.
        
        cutter = (
            cq.Workplane("XY")
            .polyline([p1, p2, p3, p1])
            .close()
            .extrude(10) # Enough to cover thickness 2.3
            .translate((0, 0, -5)) # Center the extrusion on Z=0
        )
        
        result = result.cut(cutter)

    # 3. Export
    # Filename: key_<hash>.stl
    filename = f"key_{hash_val}.stl"
    
    # Ensure directory exists (it should, but good practice inside function scope or handled externally)
    # We already created `backend/storage/keys`
    output_dir = "backend/storage/keys"
    full_path = os.path.join(output_dir, filename)
    
    # Export
    # Use 'binary' format implicitly or explicitly? CQ exporters usually handle it.
    cq.exporters.export(result, full_path, exporters.ExportTypes.STL)
    
    # Return path relative to project root or just filename?
    # Requirement: "return stl_url". 
    # DB stores "stl_path".
    # Let's return the relative part to be served by API.
    return f"storage/keys/{filename}"

if __name__ == "__main__":
    # Test stub
    pass
